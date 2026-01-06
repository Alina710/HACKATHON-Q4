"""
Main module to orchestrate the RAG book content ingestion pipeline.
"""
import logging
from typing import List, Dict
from book_ingestion.sitemap_enhanced_crawler import SitemapEnhancedCrawler
from book_ingestion.chunker import TextChunker, TextChunk
from book_ingestion.embedder import CohereEmbedder
from book_ingestion.storage import QdrantStorage


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BookIngestionPipeline:
    """
    Main class to orchestrate the entire book ingestion pipeline:
    Crawl -> Extract -> Chunk -> Embed -> Store
    """

    def __init__(self,
                 cohere_api_key: str = None,
                 qdrant_url: str = None,
                 qdrant_api_key: str = None,
                 chunk_size: int = 512,
                 overlap: int = 50,
                 crawl_delay: float = 1.0,
                 max_pages: int = 100):
        """
        Initialize the ingestion pipeline.

        Args:
            cohere_api_key: Cohere API key
            qdrant_url: Qdrant URL
            qdrant_api_key: Qdrant API key
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
            crawl_delay: Delay between crawl requests
            max_pages: Maximum number of pages to crawl
        """
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
        self.embedder = CohereEmbedder(api_key=cohere_api_key)
        self.storage = QdrantStorage(url=qdrant_url, api_key=qdrant_api_key)

        self.crawl_delay = crawl_delay
        self.max_pages = max_pages

    def run_pipeline(self, urls: List[str]) -> int:
        """
        Run the complete ingestion pipeline.

        Args:
            urls: List of URLs to crawl and ingest

        Returns:
            Number of chunks successfully ingested
        """
        logger.info(f"Starting ingestion pipeline for {len(urls)} URLs")

        # Step 1: Crawl the URLs using sitemap-enhanced crawler
        logger.info("Step 1: Crawling URLs using sitemap-enhanced crawler...")
        crawler = SitemapEnhancedCrawler(
            base_urls=urls,
            delay=self.crawl_delay,
            max_pages=self.max_pages
        )
        pages = crawler.crawl()

        if not pages:
            logger.warning("No pages were crawled. Exiting.")
            return 0

        logger.info(f"Crawled {len(pages)} pages successfully")

        # Step 2: Chunk the content
        logger.info("Step 2: Chunking content...")
        chunks = self.chunker.chunk_pages(pages)
        logger.info(f"Created {len(chunks)} text chunks")

        if not chunks:
            logger.warning("No chunks were created. Exiting.")
            return 0

        # Step 3: Generate embeddings
        logger.info("Step 3: Generating embeddings...")
        try:
            embeddings = self.embedder.embed_chunks(chunks)
            logger.info(f"Generated {len(embeddings)} embeddings")
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

        if len(embeddings) != len(chunks):
            raise ValueError(f"Mismatch between number of chunks ({len(chunks)}) and embeddings ({len(embeddings)})")

        # Step 4: Store in Qdrant
        logger.info("Step 4: Storing embeddings in Qdrant...")
        try:
            self.storage.store_embeddings(chunks, embeddings)
            logger.info("Successfully stored embeddings in Qdrant")
        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            raise

        logger.info("Ingestion pipeline completed successfully!")
        return len(chunks)

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for relevant content using a query string.

        Args:
            query: Query string to search for
            limit: Maximum number of results to return

        Returns:
            List of matching chunks with metadata
        """
        # Generate embedding for the query
        query_embedding = self.embedder.embed_single_text(query, text_type="search_query")

        # Search in Qdrant
        results = self.storage.search(query_embedding, limit=limit)

        return results


def main():
    """
    Main function to demonstrate the complete pipeline.
    """
    import os

    # Get configuration from environment variables
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not cohere_api_key:
        logger.error("COHERE_API_KEY environment variable not set")
        return

    if not qdrant_url:
        logger.error("QDRANT_URL environment variable not set")
        return

    # Initialize pipeline
    pipeline = BookIngestionPipeline(
        cohere_api_key=cohere_api_key,
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key
    )

    # Example URLs (replace with actual documentation URLs)
    urls = [
        "https://hackathon-q4-murex.vercel.app"  # Updated to use the actual site
    ]

    try:
        # Run the ingestion pipeline
        num_ingested = pipeline.run_pipeline(urls)
        print(f"Successfully ingested {num_ingested} chunks")

        # Example search
        query = "How to configure Docusaurus"
        results = pipeline.search(query, limit=3)

        print(f"\nSearch results for '{query}':")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['source_url']}")
            print(f"   Score: {result['score']:.3f}")
            print(f"   Content: {result['content'][:200]}...")
            print()

    except Exception as e:
        logger.error(f"Error running pipeline: {str(e)}")


if __name__ == "__main__":
    main()