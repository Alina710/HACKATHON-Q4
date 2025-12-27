# RAG Book Content Ingestion System

This project implements a system to crawl public Docusaurus documentation websites, extract content, generate embeddings using Cohere models, and store them in a Qdrant vector database for later retrieval.

## Features

- **Docusaurus Crawler**: Automatically discovers and crawls Docusaurus documentation sites
- **Content Extractor**: Extracts clean text content from HTML pages
- **Text Chunker**: Splits large documents into smaller, manageable chunks
- **Embedding Generator**: Creates vector embeddings using Cohere API
- **Vector Storage**: Stores embeddings in Qdrant vector database
- **Search Functionality**: Enables vector similarity search on stored content

## Architecture

The system consists of several modules:

- `crawler.py`: Handles URL crawling and content extraction
- `chunker.py`: Splits documents into semantic chunks
- `embedder.py`: Generates embeddings using Cohere API
- `storage.py`: Stores embeddings in Qdrant database
- `pipeline.py`: Orchestrates the entire ingestion process

## Prerequisites

- Python 3.9+
- Cohere API key
- Qdrant Cloud account and API key

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   export COHERE_API_KEY="your-cohere-api-key"
   export QDRANT_URL="your-qdrant-url"
   export QDRANT_API_KEY="your-qdrant-api-key"
   ```

## Configuration

The system can be configured via the `config.yaml` file:

```yaml
# Crawler settings
CRAWLER:
  DELAY: 1.0  # Delay between requests in seconds
  MAX_PAGES: 100  # Maximum number of pages to crawl per site

# Chunker settings
CHUNKER:
  CHUNK_SIZE: 512  # Maximum size of each chunk (in characters)
  OVERLAP: 50  # Number of characters to overlap between chunks

# Embedder settings
EMBEDDER:
  MODEL: "embed-english-v3.0"  # Cohere embedding model to use

# Storage settings
STORAGE:
  COLLECTION_NAME: "book_embeddings"  # Name of the Qdrant collection
```

## Usage

### Running the Ingestion Pipeline

```python
from book_ingestion.pipeline import BookIngestionPipeline

# Initialize the pipeline
pipeline = BookIngestionPipeline(
    cohere_api_key="your-cohere-api-key",
    qdrant_url="your-qdrant-url",
    qdrant_api_key="your-qdrant-api-key"
)

# Run the ingestion pipeline
urls = ["https://your-docusaurus-site.com/docs"]
num_ingested = pipeline.run_pipeline(urls)
print(f"Successfully ingested {num_ingested} chunks")
```

### Searching for Content

```python
# Search for relevant content
query = "How to configure Docusaurus"
results = pipeline.search(query, limit=5)

for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['source_url']}")
    print(f"Content: {result['content'][:200]}...")
    print(f"Score: {result['score']:.3f}")
    print("---")
```

## Testing

Run the import tests to verify all modules work correctly:

```bash
python test_imports.py
```

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL for your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)

## Project Structure

```
.
├── book_ingestion/           # Main source code
│   ├── crawler.py           # URL crawling and content extraction
│   ├── chunker.py           # Text chunking functionality
│   ├── embedder.py          # Embedding generation with Cohere
│   ├── storage.py           # Qdrant vector storage
│   └── pipeline.py          # Main orchestration pipeline
├── specs/                   # Project specifications
│   └── rag-book-ingestion/  # Feature specification and plan
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
├── test_imports.py          # Import verification tests
└── README.md               # This file
```

## Development

The system is designed to be modular and extensible. Each component can be used independently or as part of the full pipeline.