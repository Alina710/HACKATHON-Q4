# API Reference for RAG Chatbot Integration

## Base URL
The API is available at `http://localhost:8000` during development and will be deployed at a production URL in the final deployment.

## Endpoints

### GET /
**Health Check**
- **Description**: Verify that the RAG Query API is running
- **Method**: `GET`
- **Path**: `/`
- **Response**:
  ```json
  {
    "message": "RAG Query API is running"
  }
  ```

### POST /query
**Query RAG System**
- **Description**: Submit a query to the RAG system and receive a response with source citations
- **Method**: `POST`
- **Path**: `/query`
- **Content-Type**: `application/json`

#### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | The user's question or search query (1-1000 characters) |
| user_id | string | No | Identifier for the user making the request (max 100 characters) |
| session_id | string | No | Session identifier for conversation tracking (max 200 characters) |
| context | object | No | Additional context for the query |

#### Example Request
```json
{
  "query": "What are the key concepts in chapter 3?",
  "user_id": "user_123",
  "session_id": "session_456",
  "context": {
    "current_page": "/docs/chapter-2",
    "session_id": "session_456"
  }
}
```

#### Response
**Success Response (200 OK)**
```json
{
  "query_id": "string - Unique identifier for the query",
  "answer": "string - The agent's response to the query",
  "sources": [
    {
      "title": "string - Title of the source document",
      "url": "string - URL to access the source document",
      "snippet": "string - Relevant text snippet from the source",
      "page_number": "integer - Page number if from a multi-page document"
    }
  ],
  "confidence_score": "float - Confidence level of the response (0.0-1.0)",
  "timestamp": "datetime - When the response was generated",
  "session_id": "string - Session ID for conversation tracking"
}
```

**Validation Error Response (422 Unprocessable Entity)**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "query"],
      "msg": "Error message describing the validation issue",
      "input": "The invalid input value"
    }
  ]
}
```

**Rate Limit Exceeded Response (429 Too Many Requests)**
```
Rate limit exceeded: 10 requests per minute per IP address
```

**Server Error Response (500 Internal Server Error)**
```json
{
  "detail": "Error message describing the server issue"
}
```

## Rate Limiting
- The API implements rate limiting at 10 requests per minute per IP address
- Exceeding the rate limit will result in a 429 status code

## Error Codes
- `422`: Validation error - request body doesn't meet validation requirements
- `429`: Rate limit exceeded - too many requests from the same IP
- `500`: Internal server error - issue with the RAG system or server

## Validation Rules
- Query must be 1-1000 characters
- Query cannot contain SQL injection patterns
- User ID must be less than 100 characters
- Session ID must be less than 200 characters