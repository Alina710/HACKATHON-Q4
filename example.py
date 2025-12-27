"""
Example script demonstrating the usage of the RAG Book Content Ingestion system.
"""
import os
from book_ingestion.pipeline import BookIngestionPipeline


def main():
    """
    Example usage of the BookIngestionPipeline.
    """
    print("RAG Book Content Ingestion - Example Usage")
    print("=" * 50)

    # Get configuration from environment variables
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not cohere_api_key:
        print("ERROR: COHERE_API_KEY environment variable not set")
        print("Please set your Cohere API key before running this example")
        return

    if not qdrant_url:
        print("ERROR: QDRANT_URL environment variable not set")
        print("Please set your Qdrant URL before running this example")
        return

    print("Initializing the Book Ingestion Pipeline...")

    try:
        # Initialize the pipeline with configuration
        pipeline = BookIngestionPipeline(
            cohere_api_key=cohere_api_key,
            qdrant_url=qdrant_url,
            qdrant_api_key=qdrant_api_key,
            chunk_size=512,
            overlap=50,
            crawl_delay=1.0,
            max_pages=50
        )

        print("Pipeline initialized successfully!")
        print()

        # Example URLs to crawl (replace with actual documentation URLs)
        urls = [
            "https://hackathon-q4-murex.vercel.app"  # Updated to use the actual site
            # Add your actual documentation URLs here
        ]

        print(f"Starting ingestion for URLs: {urls}")
        print("Note: This will crawl the sites, extract content, chunk it,")
        print("generate embeddings, and store them in Qdrant.")
        print()

        # Uncomment the next lines to actually run the ingestion
        # num_ingested = pipeline.run_pipeline(urls)
        # print(f"Successfully ingested {num_ingested} chunks")

        print("Pipeline ready! When you have real URLs and API keys set,")
        print("uncomment the run_pipeline call in the example code to execute.")
        print()

        # Example search (this would work after ingestion)
        print("Example search functionality:")
        sample_query = "How to configure documentation settings"
        print(f"If data were ingested, searching for: '{sample_query}'")
        print("(Search functionality would return relevant content chunks)")

    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        return


if __name__ == "__main__":
    main()