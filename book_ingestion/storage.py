"""
Module for storing embeddings in Qdrant vector database.
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
import uuid
import logging
from book_ingestion.chunker import TextChunk

logger = logging.getLogger(__name__)


class QdrantStorage:
    """
    Class for storing and retrieving embeddings in Qdrant vector database.
    """

    def __init__(self, url: str = None, api_key: str = None, collection_name: str = "book_embeddings"):
        """
        Initialize the Qdrant storage.

        Args:
            url: Qdrant URL (if not provided, will try to read from QDRANT_URL env var)
            api_key: Qdrant API key (if not provided, will try to read from QDRANT_API_KEY env var)
            collection_name: Name of the collection to store embeddings
        """
        import os
        if url is None:
            url = os.getenv("QDRANT_URL")
            if not url:
                raise ValueError("Qdrant URL not provided and QDRANT_URL environment variable not set")

        if api_key is None:
            api_key = os.getenv("QDRANT_API_KEY")

        # Initialize client
        if api_key:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            # For local Qdrant instances without authentication
            self.client = QdrantClient(url=url)

        self.collection_name = collection_name
        self._ensure_collection_exists()

    def _ensure_collection_exists(self, vector_size: int = 1024):
        """
        Ensure the collection exists with the appropriate configuration.
        Default vector size of 1024 assumes Cohere's embed-english-v3.0 model.
        """
        try:
            # Try to get collection info to see if it exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception:
            # Collection doesn't exist, create it
            logger.info(f"Creating collection '{self.collection_name}'")

            # For Cohere's embed-english-v3.0 model, the default embedding size is 1024
            # but we'll make it configurable based on actual embedding size
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")

    def store_embeddings(self, chunks: List[TextChunk], embeddings: List[List[float]], batch_size: int = 64):
        """
        Store chunks and their embeddings in Qdrant.

        Args:
            chunks: List of TextChunk objects
            embeddings: List of embedding vectors corresponding to the chunks
            batch_size: Number of points to upload at once
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")

        # Prepare points for insertion
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = models.PointStruct(
                id=str(uuid.uuid4()),  # Generate unique ID
                vector=embedding,
                payload={
                    "id": chunk.id,
                    "content": chunk.content,
                    "source_url": chunk.source_url,
                    "title": chunk.title,
                    "position": chunk.position,
                    "metadata": chunk.metadata
                }
            )
            points.append(point)

            # Batch upload when we reach batch_size
            if len(points) >= batch_size:
                self.client.upsert(collection_name=self.collection_name, points=points)
                logger.info(f"Uploaded batch of {len(points)} points to Qdrant")
                points = []  # Reset for next batch

        # Upload remaining points if any
        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)
            logger.info(f"Uploaded final batch of {len(points)} points to Qdrant")

    def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """
        Search for similar chunks using a query embedding.

        Args:
            query_embedding: Embedding vector to search for
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing matching chunks and their metadata
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "content": result.payload.get("content", ""),
                "source_url": result.payload.get("source_url", ""),
                "title": result.payload.get("title", ""),
                "score": result.score,
                "metadata": result.payload.get("metadata", {})
            })

        return formatted_results

    def get_collection_info(self) -> Dict:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection information
        """
        collection_info = self.client.get_collection(self.collection_name)
        return {
            "name": collection_info.config.params.vectors_count,
            "vector_size": collection_info.config.params.vector_size,
            "points_count": collection_info.points_count
        }


def main():
    """
    Main function to demonstrate the Qdrant storage.
    Note: This requires valid Qdrant credentials.
    """
    try:
        # Initialize storage (will use QDRANT_URL and QDRANT_API_KEY from environment)
        storage = QdrantStorage()

        # Print collection info
        info = storage.get_collection_info()
        print(f"Collection info: {info}")

    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set QDRANT_URL and QDRANT_API_KEY environment variables to test Qdrant functionality.")


if __name__ == "__main__":
    main()