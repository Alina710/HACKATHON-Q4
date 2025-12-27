# Data Model: RAG System Frontend Integration

## Key Entities

### Query Request
- **Fields**:
  - `query` (string, required): The user's question or search query
  - `user_id` (string, optional): Identifier for the user making the request
  - `context` (object, optional): Additional context for the query
  - `timestamp` (datetime, optional): When the query was submitted
- **Validation**:
  - Query must be between 1-1000 characters
  - Query must not contain SQL injection patterns
- **Relationships**: None

### RAG Response
- **Fields**:
  - `answer` (string, required): The agent's response to the query
  - `sources` (array of objects, optional): List of source documents referenced
  - `confidence_score` (float, optional): Confidence level of the response (0.0-1.0)
  - `query_id` (string, required): Unique identifier for the query
  - `timestamp` (datetime, required): When the response was generated
- **Validation**:
  - Answer must not be empty
  - Confidence score must be between 0.0 and 1.0 if provided
- **Relationships**: Generated from Query Request

### Source Document Reference
- **Fields**:
  - `title` (string, required): Title of the source document
  - `url` (string, required): URL to access the source document
  - `snippet` (string, optional): Relevant text snippet from the source
  - `page_number` (integer, optional): Page number if from a multi-page document
- **Validation**:
  - URL must be a valid format
  - Title must not be empty
- **Relationships**: Part of RAG Response

## State Transitions
- Query Request: PENDING → PROCESSING → COMPLETED/ERROR
- RAG Response: Not Created → Generated → Returned to User

## API Request/Response Examples

### Query Request JSON
```json
{
  "query": "What are the key concepts in chapter 3?",
  "user_id": "user_123",
  "context": {
    "current_page": "/docs/chapter-2",
    "session_id": "session_456"
  }
}
```

### RAG Response JSON
```json
{
  "query_id": "query_789",
  "answer": "Chapter 3 covers the fundamental concepts of RAG systems...",
  "sources": [
    {
      "title": "Chapter 3: RAG Fundamentals",
      "url": "/docs/chapter-3",
      "snippet": "The retrieval-augmented generation (RAG) system combines...",
      "page_number": 1
    }
  ],
  "confidence_score": 0.92,
  "timestamp": "2025-12-27T10:30:00Z"
}
```