import asyncio
import json
from api import app, QueryRequest
from fastapi.testclient import TestClient

def test_response_formatting():
    # Create a test client for the FastAPI app
    client = TestClient(app)

    print("Testing response formatting with various scenarios...")

    # Test scenario 1: Query that should return sources
    print("\n--- Test 1: Query with expected sources ---")
    sample_query_1 = {
        "query": "What is the purpose of this system?",
        "user_id": "test_user_123",
        "context": {
            "current_page": "/docs/intro",
            "session_id": "test_session_456"
        }
    }

    response = client.post("/query", json=sample_query_1)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Answer preview: {data['answer'][:100]}...")
        print(f"Sources count: {len(data.get('sources', []))}")
        if data.get('sources'):
            print(f"First source: {data['sources'][0]}")
    else:
        print(f"Error: {response.text}")

    # Test scenario 2: Short query
    print("\n--- Test 2: Short query ---")
    sample_query_2 = {
        "query": "Hello",
        "user_id": "test_user_456"
    }

    response = client.post("/query", json=sample_query_2)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Answer preview: {data['answer'][:100]}...")
        print(f"Sources count: {len(data.get('sources', []))}")
    else:
        print(f"Error: {response.text}")

    # Test scenario 3: Query with special characters
    print("\n--- Test 3: Query with special characters ---")
    sample_query_3 = {
        "query": "How does the 'RAG' system work?",
        "user_id": "test_user_789"
    }

    response = client.post("/query", json=sample_query_3)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Answer preview: {data['answer'][:100]}...")
        print(f"Sources count: {len(data.get('sources', []))}")
    else:
        print(f"Error: {response.text}")

    print("\n--- Response Formatting Test Complete ---")

if __name__ == "__main__":
    test_response_formatting()