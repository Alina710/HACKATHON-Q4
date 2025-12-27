#!/usr/bin/env python3
"""
Retrieval script for RAG pipeline.
Connects to Qdrant, loads existing vector collections, performs similarity search,
and validates results with metadata and source URLs.
"""
import os
import logging
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QdrantRetriever:
    """
    Class for retrieving stored embeddings from Qdrant vector database.
    """

    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None, collection_name: str = "documents"):
        """
        Initialize the Qdrant retriever.

        Args:
            url: Qdrant URL (if not provided, will try to read from QDRANT_URL env var)
            api_key: Qdrant API key (if not provided, will try to read from QDRANT_API_KEY env var)
            collection_name: Name of the collection to retrieve from
        """
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
        self._validate_collection_exists()

    def _validate_collection_exists(self):
        """Validate that the specified collection exists in Qdrant."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' exists with {collection_info.points_count} vectors")
        except Exception as e:
            logger.error(f"Collection '{self.collection_name}' does not exist: {str(e)}")
            raise

    def list_collections(self) -> List[str]:
        """
        List all available collections in Qdrant.

        Returns:
            List of collection names
        """
        collections = self.client.get_collections()
        collection_names = [collection.name for collection in collections.collections]
        logger.info(f"Available collections: {collection_names}")
        return collection_names

    def get_collection_info(self) -> Dict:
        """
        Get detailed information about the current collection.

        Returns:
            Dictionary with collection information
        """
        collection_info = self.client.get_collection(self.collection_name)
        info = {
            "name": self.collection_name,
            "points_count": collection_info.points_count,
            "config": {
                "distance": collection_info.config.params.vectors.get("size", None) if hasattr(collection_info.config.params.vectors, 'get') else "unknown",
                "distance_type": collection_info.config.params.vectors.get("distance", None) if hasattr(collection_info.config.params.vectors, 'get') else "unknown"
            }
        }
        return info

    def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """
        Search for similar documents using a query embedding.

        Args:
            query_embedding: Embedding vector to search for
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing matching documents and their metadata
        """
        results = self.client.query_points(
    collection_name=self.collection_name,
    query=query_embedding,
    limit=limit,
    with_payload=True
).points

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "content": result.payload.get("content", ""),
                "source_url": result.payload.get("source_url", ""),
                "title": result.payload.get("title", ""),
                "score": result.score,
                "chunk_index": result.payload.get("chunk_index", 0),
                "metadata": result.payload.get("metadata", {})
            })

        return formatted_results


class CohereEmbedder:
    """
    Class for generating embeddings using Cohere API.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Cohere embedder.

        Args:
            api_key: Cohere API key (if not provided, will try to read from COHERE_API_KEY env var)
        """
        if api_key is None:
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("Cohere API key not provided and COHERE_API_KEY environment variable not set")

        self.client = cohere.Client(api_key)
        self.model = "embed-english-v3.0"

    def embed_text(self, text: str, text_type: str = "search_query") -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed
            text_type: Type of text (search_query, search_document, etc.)

        Returns:
            Embedding vector as a list of floats
        """
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type=text_type
        )
        return response.embeddings[0]


class Retriever:
    """
    Main retrieval class that combines Qdrant and Cohere functionality.
    """

    def __init__(self,
                 qdrant_url: Optional[str] = None,
                 qdrant_api_key: Optional[str] = None,
                 cohere_api_key: Optional[str] = None,
                 collection_name: str = "documents"):
        """
        Initialize the retriever.

        Args:
            qdrant_url: Qdrant URL
            qdrant_api_key: Qdrant API key
            cohere_api_key: Cohere API key
            collection_name: Name of the collection to search in
        """
        self.qdrant_retriever = QdrantRetriever(
            url=qdrant_url,
            api_key=qdrant_api_key,
            collection_name=collection_name
        )
        self.embedder = CohereEmbedder(api_key=cohere_api_key)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve top-k similar documents for a given query.

        Args:
            query: Search query string
            top_k: Number of top results to return

        Returns:
            List of dictionaries containing retrieved documents with metadata
        """
        logger.info(f"Retrieving top {top_k} results for query: '{query}'")

        # Generate embedding for the query
        query_embedding = self.embedder.embed_text(query, text_type="search_query")
        logger.info(f"Generated embedding with {len(query_embedding)} dimensions")

        # Search in Qdrant
        results = self.qdrant_retriever.search(query_embedding, limit=top_k)
        logger.info(f"Retrieved {len(results)} results from Qdrant")

        return results

    def validate_results(self, results: List[Dict], query: str) -> Dict:
        """
        Validate the retrieved results.

        Args:
            results: List of retrieved documents
            query: Original query string

        Returns:
            Dictionary with validation results
        """
        validation = {
            "query": query,
            "result_count": len(results),
            "valid_results": 0,
            "invalid_results": 0,
            "validation_details": [],
            "all_results_valid": True
        }

        for i, result in enumerate(results):
            result_validation = {
                "index": i,
                "has_content": bool(result.get("content")),
                "has_source_url": bool(result.get("source_url")),
                "has_title": bool(result.get("title")),
                "has_score": result.get("score") is not None,
                "has_metadata": result.get("metadata") is not None,
                "content_length": len(result.get("content", "")),
                "valid": True
            }

            # Check if all required fields are present
            required_fields_valid = (
                result_validation["has_content"] and
                result_validation["has_source_url"] and
                result_validation["has_title"] and
                result_validation["has_score"]
            )

            result_validation["valid"] = required_fields_valid
            validation["validation_details"].append(result_validation)

            if result_validation["valid"]:
                validation["valid_results"] += 1
            else:
                validation["invalid_results"] += 1
                validation["all_results_valid"] = False

        logger.info(f"Validation: {validation['valid_results']}/{len(results)} results are valid")
        return validation


def main():
    """
    Main function to demonstrate the retrieval functionality.
    """
    logger.info("Starting RAG retrieval pipeline...")

    try:
        # Initialize the retriever
        retriever = Retriever(
            collection_name="documents"  # Default collection name, can be changed
        )

        # Get collection info
        collection_info = retriever.qdrant_retriever.get_collection_info()
        logger.info(f"Collection info: {collection_info}")

        # Example queries for testing
        test_queries = [
            "What is ROS 2?",
            "Docusaurus documentation",
            "How to configure the system",
            "getting started guide",
            "API reference"
        ]

        # Perform retrieval for each query
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print('='*60)

            # Retrieve results
            results = retriever.retrieve(query, top_k=3)

            # Validate results
            validation = retriever.validate_results(results, query)

            print(f"Retrieved {len(results)} results")
            print(f"Validation: {validation['valid_results']} valid, {validation['invalid_results']} invalid")

            # Display results
            for i, result in enumerate(results, 1):
                print(f"\nResult {i} (Score: {result['score']:.4f}):")
                print(f"  Title: {result['title'][:100]}...")
                print(f"  URL: {result['source_url']}")
                print(f"  Content snippet: {result['content'][:200]}...")
                print(f"  Content length: {len(result['content'])} chars")
                print(f"  Chunk index: {result['chunk_index']}")

            if not results:
                print("  No results found for this query.")

        print(f"\n{'='*60}")
        print("Retrieval pipeline completed successfully!")
        print('='*60)

    except Exception as e:
        logger.error(f"Error in retrieval pipeline: {str(e)}")
        raise


if __name__ == "__main__":
    main()