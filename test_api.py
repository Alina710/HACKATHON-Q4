import asyncio
import json
from api import app, QueryRequest
from fastapi.testclient import TestClient

def test_api():
    # Create a test client for the FastAPI app
    client = TestClient(app)

    print("Testing API endpoints...")

    # Test the root endpoint
    response = client.get("/")
    print(f"Root endpoint status: {response.status_code}")
    print(f"Root endpoint response: {response.json()}")

    # Test the query endpoint with a sample request
    sample_query = {
        "query": "What is the purpose of this system?",
        "user_id": "test_user_123",
        "context": {
            "current_page": "/docs/intro",
            "session_id": "test_session_456"
        }
    }

    response = client.post("/query", json=sample_query)
    print(f"Query endpoint status: {response.status_code}")
    if response.status_code == 200:
        print(f"Query response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Query error: {response.text}")

if __name__ == "__main__":
    test_api()