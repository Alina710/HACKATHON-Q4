"""
URL Ingestion & Embedding Pipeline
This script fetches URLs, cleans text, chunks it, generates embeddings using Cohere,
and stores them in Qdrant Cloud.
"""
import asyncio
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
import re
import uuid
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """Represents a chunk of a document with its metadata."""
    id: str
    content: str
    source_url: str
    title: str
    chunk_index: int
    metadata: Dict[str, str]


class TextCleaner:
    """Handles cleaning and preprocessing of text content."""

    @staticmethod
    def clean_html_content(html: str) -> str:
        """Extract and clean text content from HTML."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    @staticmethod
    def clean_text(text: str) -> str:
        """Apply general text cleaning."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', ' ', text)
        return text.strip()


class TextChunker:
    """Handles chunking of large text documents."""

    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, source_url: str, title: str) -> List[DocumentChunk]:
        """Chunk text into smaller pieces."""
        chunks = []

        # Split text into sentences to maintain semantic boundaries
        sentences = re.split(r'[.!?]+', text)

        current_chunk = ""
        chunk_index = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # If adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk.strip():
                    # Save the current chunk
                    chunk_id = f"{source_url}#{chunk_index}"
                    chunks.append(DocumentChunk(
                        id=chunk_id,
                        content=current_chunk.strip(),
                        source_url=source_url,
                        title=title,
                        chunk_index=chunk_index,
                        metadata={"chunk_size": str(len(current_chunk))}
                    ))
                    chunk_index += 1

                # Start a new chunk with overlap
                if len(sentence) > self.chunk_size:
                    # If the sentence itself is too long, split it
                    for i in range(0, len(sentence), self.chunk_size - self.overlap):
                        chunk_part = sentence[i:i + self.chunk_size - self.overlap]
                        chunk_id = f"{source_url}#{chunk_index}"
                        chunks.append(DocumentChunk(
                            id=chunk_id,
                            content=chunk_part.strip(),
                            source_url=source_url,
                            title=title,
                            chunk_index=chunk_index,
                            metadata={"chunk_size": str(len(chunk_part))}
                        ))
                        chunk_index += 1
                else:
                    # Start new chunk with some overlap from the previous chunk
                    if self.overlap > 0 and len(current_chunk) > self.overlap:
                        current_chunk = current_chunk[-self.overlap:] + " " + sentence
                    else:
                        current_chunk = sentence
            else:
                current_chunk += " " + sentence

        # Add the last chunk if it exists
        if current_chunk.strip():
            chunk_id = f"{source_url}#{chunk_index}"
            chunks.append(DocumentChunk(
                id=chunk_id,
                content=current_chunk.strip(),
                source_url=source_url,
                title=title,
                chunk_index=chunk_index,
                metadata={"chunk_size": str(len(current_chunk))}
            ))

        return chunks


class URLFetcher:
    """Handles fetching content from URLs."""

    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; URLIngestionBot/1.0; +http://example.com/bot)'
        })

    def fetch_url(self, url: str) -> Optional[Dict[str, str]]:
        """Fetch content from a single URL."""
        try:
            logger.info(f"Fetching URL: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Parse the HTML to extract title and content
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"

            return {
                'url': url,
                'title': title.strip(),
                'content': response.text
            }
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def fetch_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """Fetch content from multiple URLs."""
        results = []
        for url in urls:
            result = self.fetch_url(url)
            if result:
                results.append(result)
            # Be respectful with delays
            import time
            time.sleep(self.delay)
        return results


class Embedder:
    """Handles generating embeddings using Cohere."""

    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("Cohere API key not provided and COHERE_API_KEY environment variable not set")

        self.client = cohere.Client(api_key)
        self.model = "embed-english-v3.0"  # Using the latest model

    def embed_texts(self, texts: List[str], text_type: str = "search_document") -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        if not texts:
            return []

        # Cohere has a limit on batch size, so we'll process in chunks
        batch_size = 96  # Max batch size for Cohere
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"Embedding batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

            try:
                response = self.client.embed(
                    texts=batch,
                    model=self.model,
                    input_type=text_type
                )
                all_embeddings.extend(response.embeddings)
            except Exception as e:
                logger.error(f"Error embedding batch: {str(e)}")
                raise

        return all_embeddings


class QdrantStorage:
    """Handles storing embeddings in Qdrant Cloud."""

    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None, collection_name: str = "documents"):
        if url is None:
            url = os.getenv("QDRANT_URL")
            if not url:
                raise ValueError("Qdrant URL not provided and QDRANT_URL environment variable not set")

        if api_key is None:
            api_key = os.getenv("QDRANT_API_KEY")

        # Initialize Qdrant client
        if api_key:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            self.client = QdrantClient(url=url)

        self.collection_name = collection_name
        self._create_collection()

    def _create_collection(self):
        """Create the collection if it doesn't exist."""
        try:
            # Try to get the collection to see if it exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except:
            # Collection doesn't exist, create it
            # For Cohere's embed-english-v3.0, the embedding size is 1024
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
            )
            logger.info(f"Created collection '{self.collection_name}'")

    def store_embeddings(self, chunks: List[DocumentChunk], embeddings: List[List[float]]):
        """Store document chunks and their embeddings in Qdrant."""
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")

        # Prepare points for insertion
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "id": chunk.id,
                    "content": chunk.content,
                    "source_url": chunk.source_url,
                    "title": chunk.title,
                    "chunk_index": chunk.chunk_index,
                    "metadata": chunk.metadata
                }
            )
            points.append(point)

        # Upload points to Qdrant
        self.client.upsert(collection_name=self.collection_name, points=points)
        logger.info(f"Stored {len(points)} embeddings in Qdrant collection '{self.collection_name}'")

    def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """Search for similar documents based on embedding."""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )

        return [
            {
                "id": result.id,
                "content": result.payload.get("content", ""),
                "source_url": result.payload.get("source_url", ""),
                "title": result.payload.get("title", ""),
                "score": result.score,
                "chunk_index": result.payload.get("chunk_index", 0)
            }
            for result in results
        ]


class IngestionPipeline:
    """Main pipeline class that orchestrates the entire process."""

    def __init__(self):
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()
        self.fetcher = URLFetcher()

        # These will be initialized only when needed to avoid errors without API keys
        self.embedder = None
        self.storage = None

    def initialize_services(self):
        """Initialize services that require API keys."""
        self.embedder = Embedder()
        self.storage = QdrantStorage()

    def process_urls(self, urls: List[str]) -> int:
        """Process a list of URLs end-to-end."""
        logger.info(f"Starting ingestion pipeline for {len(urls)} URLs")

        # Step 1: Fetch URLs
        logger.info("Step 1: Fetching URLs...")
        raw_data = self.fetcher.fetch_urls(urls)

        if not raw_data:
            logger.error("No data fetched from URLs")
            return 0

        # Step 2: Clean and extract content
        logger.info("Step 2: Cleaning and extracting content...")
        documents = []
        for item in raw_data:
            clean_content = self.cleaner.clean_html_content(item['content'])
            clean_content = self.cleaner.clean_text(clean_content)
            documents.append({
                'url': item['url'],
                'title': item['title'],
                'content': clean_content
            })

        # Step 3: Chunk documents
        logger.info("Step 3: Chunking documents...")
        all_chunks = []
        for doc in documents:
            chunks = self.chunker.chunk_text(doc['content'], doc['url'], doc['title'])
            all_chunks.extend(chunks)

        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")

        if not all_chunks:
            logger.error("No chunks created from documents")
            return 0

        # Initialize services that require API keys
        self.initialize_services()

        # Step 4: Generate embeddings
        logger.info("Step 4: Generating embeddings...")
        texts = [chunk.content for chunk in all_chunks]
        embeddings = self.embedder.embed_texts(texts)

        logger.info(f"Generated {len(embeddings)} embeddings")

        # Step 5: Store in Qdrant
        logger.info("Step 5: Storing embeddings in Qdrant...")
        self.storage.store_embeddings(all_chunks, embeddings)

        logger.info("Ingestion pipeline completed successfully!")
        return len(all_chunks)


def main():
    """Main function to run the full ingestion pipeline end-to-end."""
    # Example URLs - replace with actual URLs you want to process
    urls = [
        "https://hackathon-q4-murex.vercel.app/docs/intro",
        "https://hackathon-q4-murex.vercel.app/docs/module-1-ros2-nervous-system/introduction-to-ros2",
        "https://hackathon-q4-murex.vercel.app/docs/module-1-ros2-nervous-system/robot-structure-urdf",
        "https://hackathon-q4-murex.vercel.app/docs/module-1-ros2-nervous-system/communication-model",
        "https://hackathon-q4-murex.vercel.app/docs/module2/chapter1",
        "https://hackathon-q4-murex.vercel.app/docs/module2/chapter2",
        "https://hackathon-q4-murex.vercel.app/docs/module2/chapter3",
        "https://hackathon-q4-murex.vercel.app/docs/module3/chapter1",
        "https://hackathon-q4-murex.vercel.app/docs/module3/chapter2",
        "https://hackathon-q4-murex.vercel.app/docs/module3/chapter3",
        "https://hackathon-q4-murex.vercel.app/docs/module4/chapter1",
        "https://hackathon-q4-murex.vercel.app/docs/module4/chapter2",
        "https://hackathon-q4-murex.vercel.app/docs/module4/chapter3",
         

            # Replace with actual documentation URLs
        # Add more URLs as needed
    ]

    if not urls:
        logger.warning("No URLs provided. Please update the urls list with actual documentation URLs.")
        return

    # Check for required environment variables
    if not os.getenv("COHERE_API_KEY"):
        logger.error("COHERE_API_KEY environment variable not set")
        return

    if not os.getenv("QDRANT_URL"):
        logger.error("QDRANT_URL environment variable not set")
        return

    # Create and run the pipeline
    pipeline = IngestionPipeline()

    try:
        num_processed = pipeline.process_urls(urls)
        print(f"Successfully processed {num_processed} document chunks")

        # Example search after ingestion
        print("\nExample search functionality:")
        if pipeline.embedder and pipeline.storage:
            query = "sample search query"
            try:
                query_embedding = pipeline.embedder.embed_texts([query], text_type="search_query")[0]
                results = pipeline.storage.search(query_embedding, limit=3)

                print(f"Search results for '{query}':")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['title'][:50]}... (Score: {result['score']:.3f})")
                    print(f"   URL: {result['source_url']}")
                    print(f"   Snippet: {result['content'][:100]}...")
                    print()
            except Exception as e:
                logger.error(f"Error during search: {e}")

    except Exception as e:
        logger.error(f"Error running ingestion pipeline: {e}")


if __name__ == "__main__":
    main()