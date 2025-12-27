"""
Test script for vector search functionality.
"""
import os
import logging
from book_ingestion.pipeline import BookIngestionPipeline

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_search_functionality():
    """
    Test the search functionality of the ingestion pipeline.
    """
    # Get configuration from environment variables
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not cohere_api_key:
        logger.error("COHERE_API_KEY environment variable not set")
        return False

    if not qdrant_url:
        logger.error("QDRANT_URL environment variable not set")
        return False

    try:
        # Initialize pipeline
        pipeline = BookIngestionPipeline(
            cohere_api_key=cohere_api_key,
            qdrant_url=qdrant_url,
            qdrant_api_key=qdrant_api_key
        )

        # Test search functionality with a sample query
        test_queries = [
            "How to configure documentation",
            "installation guide",
            "getting started",
            "API reference"
        ]

        print("Testing search functionality...")
        for query in test_queries:
            print(f"\nSearching for: '{query}'")
            results = pipeline.search(query, limit=3)

            if results:
                print(f"Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. Score: {result['score']:.3f}")
                    print(f"     Title: {result['title'][:60]}...")
                    print(f"     URL: {result['source_url']}")
                    print(f"     Snippet: {result['content'][:100]}...")
                    print()
            else:
                print("  No results found.")

        return True

    except Exception as e:
        logger.error(f"Error testing search functionality: {str(e)}")
        return False


def test_pipeline_integration():
    """
    Test the complete pipeline with sample data.
    """
    # Get configuration from environment variables
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not cohere_api_key or not qdrant_url:
        logger.error("COHERE_API_KEY and QDRANT_URL environment variables must be set")
        return False

    try:
        # Initialize pipeline
        pipeline = BookIngestionPipeline(
            cohere_api_key=cohere_api_key,
            qdrant_url=qdrant_url,
            qdrant_api_key=qdrant_api_key
        )

        # Test with a sample query to make sure the pipeline components work together
        sample_query = "test search query"
        results = pipeline.search(sample_query, limit=1)

        print(f"Integration test with query '{sample_query}':")
        if results:
            print(f"  Success: Got {len(results)} results")
            return True
        else:
            print("  Success: Got 0 results (expected if no data is ingested yet)")
            return True

    except Exception as e:
        logger.error(f"Error in integration test: {str(e)}")
        return False


def main():
    """
    Main function to run all tests.
    """
    print("Running vector search functionality tests...\n")

    # Test search functionality
    search_success = test_search_functionality()
    print(f"Search functionality test: {'PASSED' if search_success else 'FAILED'}\n")

    # Test pipeline integration
    integration_success = test_pipeline_integration()
    print(f"Pipeline integration test: {'PASSED' if integration_success else 'FAILED'}\n")

    overall_success = search_success and integration_success
    print(f"Overall test result: {'PASSED' if overall_success else 'FAILED'}")

    return overall_success


if __name__ == "__main__":
    main()