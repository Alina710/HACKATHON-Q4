# URL Ingestion & Embedding Pipeline

This project implements a complete pipeline for fetching URLs, cleaning and chunking text content, generating embeddings using Cohere, and storing them in Qdrant Cloud.

## Features

- **URL Fetching**: Fetches content from provided URLs with respectful delays
- **HTML Cleaning**: Extracts clean text content from HTML pages
- **Text Chunking**: Splits large documents into manageable chunks with overlap
- **Embedding Generation**: Creates vector embeddings using Cohere's models
- **Vector Storage**: Stores embeddings in Qdrant Cloud with metadata
- **Full Pipeline**: End-to-end processing from URLs to vector storage

## Architecture

The system consists of several key components:

- `TextCleaner`: Handles HTML parsing and text cleaning
- `TextChunker`: Splits documents into semantic chunks
- `URLFetcher`: Fetches content from URLs with proper headers
- `Embedder`: Generates embeddings using Cohere API
- `QdrantStorage`: Stores embeddings in Qdrant vector database
- `IngestionPipeline`: Orchestrates the entire process

## Prerequisites

- Python 3.8+
- Cohere API key
- Qdrant Cloud account and URL

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   export COHERE_API_KEY="your-cohere-api-key"
   export QDRANT_URL="your-qdrant-url"
   export QDRANT_API_KEY="your-qdrant-api-key"  # if required
   ```

## Usage

### Running the Full Pipeline

```python
from main import IngestionPipeline

# Create and run the pipeline
pipeline = IngestionPipeline()
urls = [
    "https://example.com/docs",
    # Add your documentation URLs here
]

num_processed = pipeline.process_urls(urls)
print(f"Processed {num_processed} document chunks")
```

### Individual Components

You can also use individual components:

```python
from main import TextCleaner, TextChunker, URLFetcher

# Clean HTML content
cleaner = TextCleaner()
clean_text = cleaner.clean_html_content(html_content)

# Chunk text
chunker = TextChunker(chunk_size=512, overlap=50)
chunks = chunker.chunk_text(text, source_url, title)

# Fetch URLs
fetcher = URLFetcher(delay=1.0)
data = fetcher.fetch_urls(urls)
```

## Configuration

The pipeline can be configured with:

- `chunk_size`: Size of text chunks (default: 512)
- `overlap`: Overlap between chunks (default: 50)
- `delay`: Delay between URL fetches (default: 1.0s)

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL for your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)

## Project Structure

```
backend/
├── main.py          # Main ingestion pipeline implementation
├── retrieve.py      # Retrieval functionality for RAG pipeline
├── requirements.txt # Python dependencies
└── README.md       # This file
```

## New Feature: Retrieval Pipeline

The `retrieve.py` script provides a complete retrieval system for the RAG (Retrieval-Augmented Generation) pipeline. It connects to Qdrant vector database, loads existing vector collections, performs similarity search, and validates results with metadata and source URLs.

### Features

- **Qdrant Connection**: Connects to Qdrant vector database with proper authentication
- **Collection Management**: Lists available collections and provides detailed information about vector collections
- **Top-K Similarity Search**: Performs semantic search using vector embeddings with configurable result count
- **Cohere Integration**: Generates query embeddings using Cohere's embedding models
- **Result Validation**: Validates retrieved results for completeness and correctness
- **Metadata Support**: Returns complete metadata including content, source URLs, titles, scores, and additional metadata

### Usage

```python
from retrieve import Retriever

# Initialize the retriever
retriever = Retriever(
    collection_name="documents"  # specify your collection name
)

# Perform retrieval
results = retriever.retrieve("your search query", top_k=5)

# Validate results
validation = retriever.validate_results(results, "your search query")
```

## Testing

Run the test script to verify the implementation:

```bash
python test_backend.py
```

## Error Handling

The pipeline includes comprehensive error handling for:
- Network issues during URL fetching
- API errors from Cohere
- Connection issues with Qdrant
- Invalid input validation