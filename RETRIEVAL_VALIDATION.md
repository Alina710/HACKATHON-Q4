# RAG Retrieval Pipeline Validation

This script validates the RAG (Retrieval-Augmented Generation) retrieval pipeline to ensure that stored embeddings can be properly retrieved from the Qdrant vector database.

## Overview

The validation script (`validate_retrieval.py`) performs comprehensive testing of the retrieval pipeline:

1. **Connection Validation**: Verifies connectivity to Qdrant vector database
2. **Search Functionality**: Tests search with various query types
3. **Metadata Validation**: Ensures retrieved results contain all expected metadata
4. **Quality Validation**: Assesses relevance of retrieved results
5. **End-to-End Validation**: Tests complete pipeline including data ingestion and retrieval

## Requirements

- Python 3.7+
- Required Python packages (from the existing project)
- Cohere API key for generating embeddings
- Qdrant vector database instance

## Environment Variables

Set the following environment variables before running:

```bash
export COHERE_API_KEY="your-cohere-api-key"
export QDRANT_URL="your-qdrant-url"  # e.g., http://localhost:6333 or https://your-qdrant-instance.com
export QDRANT_API_KEY="your-qdrant-api-key"  # if authentication is required
```

## Usage

### Basic Validation

```bash
python validate_retrieval.py
```

### Manual Testing

```python
from validate_retrieval import RetrievalPipelineValidator

validator = RetrievalPipelineValidator()
results = validator.run_comprehensive_validation()

# For end-to-end validation including data ingestion:
results = validator.run_end_to_end_validation()
```

## Validation Components

### 1. Connection Validation
- Tests connectivity to Qdrant
- Checks collection existence and status
- Reports number of stored vectors

### 2. Search Functionality
- Tests various query types against stored embeddings
- Measures query response times
- Validates result structure and completeness
- Tests with documentation-related queries

### 3. Metadata Validation
- Ensures retrieved results contain required fields:
  - `content`: The text content
  - `source_url`: Original URL of the content
  - `title`: Document title
  - `score`: Relevance score
  - `metadata`: Additional metadata

### 4. Quality Validation
- Tests semantic relevance of results
- Uses keyword matching to assess result quality
- Validates that relevant content is returned for relevant queries

## Expected Output

The validation provides detailed logging and a summary report:

```
VALIDATION SUMMARY
Pipeline setup: ✓
Connection validation: ✓
Search functionality: ✓
Metadata validation: ✓
Quality validation: ✓
Overall validation: ✓
```

## Integration with Existing Pipeline

The validation script leverages the existing `BookIngestionPipeline` from `book_ingestion/pipeline.py`:

- Uses the same `QdrantStorage` for vector storage and retrieval
- Employs the same `CohereEmbedder` for generating query embeddings
- Maintains consistency with the existing ingestion pipeline architecture

## Success Criteria

- ✅ Successfully connects to Qdrant vector database
- ✅ Valid search results returned with proper metadata
- ✅ All components work together in end-to-end pipeline
- ✅ Results match source URLs and content as expected
- ✅ Pipeline operates without errors
- ✅ Search performance meets acceptable response time thresholds