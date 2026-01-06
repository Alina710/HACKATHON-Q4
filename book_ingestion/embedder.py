"""
Module for generating embeddings using Cohere API.
"""
import cohere
from typing import List, Dict
import os
import logging
from book_ingestion.chunker import TextChunk

logger = logging.getLogger(__name__)


class CohereEmbedder:
    """
    Class for generating embeddings using Cohere API.
    """

    def __init__(self, api_key: str = None, model: str = "embed-english-v3.0"):
        """
        Initialize the embedder.

        Args:
            api_key: Cohere API key (if not provided, will try to read from COHERE_API_KEY env var)
            model: Cohere embedding model to use
        """
        if api_key is None:
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("Cohere API key not provided and COHERE_API_KEY environment variable not set")

        self.client = cohere.Client(api_key)
        self.model = model

    def embed_chunks(self, chunks: List[TextChunk], text_type: str = "search_document") -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks.

        Args:
            chunks: List of TextChunk objects to embed
            text_type: Type of text being embedded (affects embedding quality)

        Returns:
            List of embedding vectors (each is a list of floats)
        """
        if not chunks:
            return []

        # Extract just the content for embedding
        texts = [chunk.content for chunk in chunks]

        # Generate embeddings in batches to respect API limits
        embeddings = []
        batch_size = 96  # Cohere's max batch size is 96

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            logger.info(f"Embedding batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

            try:
                response = self.client.embed(
                    texts=batch,
                    model=self.model,
                    input_type=text_type
                )

                embeddings.extend(response.embeddings)

            except Exception as e:
                logger.error(f"Error embedding batch {i//batch_size + 1}: {str(e)}")
                raise

        return embeddings

    def embed_single_text(self, text: str, text_type: str = "search_document") -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed
            text_type: Type of text being embedded

        Returns:
            Embedding vector (list of floats)
        """
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type=text_type
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Error embedding single text: {str(e)}")
            raise


def main():
    """
    Main function to demonstrate the embedder.
    Note: This requires a valid Cohere API key.
    """
    # Example usage (requires valid API key)
    try:
        # Initialize embedder (will use COHERE_API_KEY from environment)
        embedder = CohereEmbedder()

        # Sample chunks to embed
        from book_ingestion.chunker import TextChunk

        sample_chunks = [
            TextChunk(
                id="test1",
                content="This is the first sample text to embed",
                source_url="https://example.com",
                title="Sample Document",
                position=0,
                metadata={}
            ),
            TextChunk(
                id="test2",
                content="This is the second sample text to embed",
                source_url="https://example.com",
                title="Sample Document",
                position=1,
                metadata={}
            )
        ]

        # Generate embeddings
        embeddings = embedder.embed_chunks(sample_chunks)

        print(f"Generated {len(embeddings)} embeddings")
        print(f"First embedding length: {len(embeddings[0])}")
        print(f"First few values of first embedding: {embeddings[0][:5]}...")

    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set COHERE_API_KEY environment variable to test embedding functionality.")


if __name__ == "__main__":
    main()