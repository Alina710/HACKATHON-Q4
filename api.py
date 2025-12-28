from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any
import logging
import uuid
import time
from datetime import datetime
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import the existing agent for RAG functionality
import asyncio
from threading import Thread

try:
    from agent import RAGAgent
    from backend.retrieve import Retriever

    # Create agent instance
    agent_instance = RAGAgent()

    # Helper function to run the agent query in a separate thread to avoid event loop conflicts
    def run_agent_query(query):
        result_container = [None]  # Use a list to store result from thread
        exception_container = [None]  # Use a list to store exception from thread

        def run_in_thread():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = agent_instance.query(query)
                result_container[0] = result
            except Exception as e:
                exception_container[0] = e
            finally:
                try:
                    loop.close()
                except:
                    pass

        # Run the agent query in a separate thread
        thread = Thread(target=run_in_thread)
        thread.start()
        thread.join(timeout=30)  # 30 second timeout

        if thread.is_alive():
            return {
                "status": "error",
                "response": "Query timeout",
                "sources": []
            }

        # Check if there was an exception in the thread
        if exception_container[0]:
            return {
                "status": "error",
                "response": f"Agent error: {str(exception_container[0])}",
                "sources": []
            }

        # Get the result from the thread
        agent_result = result_container[0]

        if agent_result and agent_result["status"] == "success":
            # Extract the response from the agent
            agent_response = agent_result["response"]

            # Now get the sources from the retrieval system
            try:
                retriever = Retriever()
                retrieval_results = retriever.retrieve(query, top_k=3)

                # Format the sources according to our data model
                formatted_sources = []
                for result in retrieval_results:
                    formatted_sources.append({
                        "title": result.get("title", "Unknown Title"),
                        "url": result.get("source_url", ""),
                        "snippet": result.get("content", "")[:200] + "..." if len(result.get("content", "")) > 200 else result.get("content", ""),
                        "page_number": result.get("chunk_index", 1)
                    })

                return {
                    "status": "success",
                    "response": agent_response,
                    "sources": formatted_sources
                }
            except Exception as e:
                print(f"Retrieval error: {e}")
                return {
                    "status": "success",
                    "response": agent_response,
                    "sources": []  # Return agent response even if sources retrieval fails
                }
        else:
            # Handle agent errors
            return {
                "status": "error",
                "response": agent_result.get("response", "Sorry, there was an error processing your query.") if agent_result else "Sorry, there was an error processing your query.",
                "sources": []
            }

except ImportError as e:
    # If agent is not available in this context, we'll handle it gracefully
    # This import may need to be adjusted based on the actual agent.py structure
    RAGAgent = None
    agent_instance = None
    run_agent_query = None
    print(f"Warning: agent module not found: {e}. This may be expected during initial setup.")
except ValueError as e:
    # Handle environment variable errors (like missing API keys)
    RAGAgent = None
    agent_instance = None
    run_agent_query = None
    print(f"Warning: Environment configuration error: {e}. Please check your .env file contains all required variables (OPENROUTER_API_KEY, COHERE_API_KEY, QDRANT_URL).")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="RAG Query API",
    description="API for querying RAG system with document retrieval capabilities",
    version="1.0.0"
)

# Add the limiter to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Pydantic models based on the data model specification
class SourceDocumentReference(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None
    page_number: Optional[int] = None

# In-memory session storage (in production, use Redis or database)
session_storage = {}

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None  # For conversation tracking
    context: Optional[Dict[str, Any]] = None

    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty')
        if len(v) > 1000:
            raise ValueError('Query must be less than 1000 characters')
        # Basic SQL injection prevention
        sql_injection_patterns = [
            'drop ', 'delete ', 'update ', 'insert ', 'exec ', 'script', '<script'
        ]
        if any(pattern in v.lower() for pattern in sql_injection_patterns):
            raise ValueError('Query contains invalid characters or patterns')
        return v.strip()

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError('User ID must be less than 100 characters')
        return v

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v):
        if v is not None and len(v) > 200:
            raise ValueError('Session ID must be less than 200 characters')
        return v

class RAGResponse(BaseModel):
    query_id: str
    answer: str
    sources: Optional[List[SourceDocumentReference]] = []
    confidence_score: Optional[float] = None
    timestamp: datetime
    session_id: str  # Include session ID in response for frontend tracking

@app.get("/")
async def root():
    return {"message": "RAG Query API is running"}

@app.post("/query", response_model=RAGResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def query_endpoint(query_request: QueryRequest, request: Request):
    """
    Process a user query against the RAG system and return a response with sources.
    """
    logger.info(f"Received query from user {query_request.user_id}: {query_request.query[:50]}...")

    # Validate query length
    if len(query_request.query) < 1 or len(query_request.query) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Query must be between 1 and 1000 characters"
        )

    # Validate query content (basic injection check)
    if any(injection_pattern in query_request.query.lower() for injection_pattern in
           ["drop ", "delete ", "update ", "insert ", "exec ", "script", "<script"]):
        raise HTTPException(
            status_code=400,
            detail="Query contains invalid characters or patterns"
        )

    # Generate or retrieve session ID
    session_id = query_request.session_id or str(uuid.uuid4())
    if session_id not in session_storage:
        session_storage[session_id] = []

    # Add current query to session history
    session_storage[session_id].append({
        "query_id": str(uuid.uuid4()),
        "query": query_request.query,
        "timestamp": datetime.utcnow()
    })

    # Limit session history to last 10 interactions to prevent memory issues
    if len(session_storage[session_id]) > 10:
        session_storage[session_id] = session_storage[session_id][-10:]

    # Generate query ID
    query_id = str(uuid.uuid4())

    try:
        # Call the RAG agent to process the query
        if run_agent_query is None:
            # For initial testing without the actual agent
            response_data = {
                "answer": f"Mock response for query: {query_request.query}",
                "sources": [
                    {
                        "title": "Mock Document",
                        "url": "/docs/mock",
                        "snippet": "This is a mock response for testing purposes",
                        "page_number": 1
                    }
                ],
                "confidence_score": 0.8
            }
        else:
            # Call the actual agent using the thread-safe function
            result = run_agent_query(query_request.query)
            if result["status"] == "success":
                # Extract answer from the agent response
                answer = result["response"]
                # Extract sources from the agent response
                sources = result.get("sources", [])
                confidence_score = result.get("confidence_score", 0.8)  # Default confidence score
                response_data = {
                    "answer": answer,
                    "sources": sources,
                    "confidence_score": confidence_score
                }
            else:
                # Handle agent errors
                response_data = {
                    "answer": "Sorry, there was an error processing your query.",
                    "sources": [],
                    "confidence_score": 0.0
                }

        # Create response object
        response = RAGResponse(
            query_id=query_id,
            answer=response_data["answer"],
            sources=response_data["sources"],
            confidence_score=response_data["confidence_score"],
            timestamp=datetime.utcnow(),
            session_id=session_id
        )

        logger.info(f"Successfully processed query {query_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing query {query_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)