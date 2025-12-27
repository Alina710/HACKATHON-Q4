import json
from api import app
from fastapi.testclient import TestClient

def test_error_handling():
    # Create a test client for the FastAPI app
    client = TestClient(app)

    print("Testing error handling scenarios...")

    # Test scenario 1: Empty query (should fail validation)
    print("\n--- Test 1: Empty query ---")
    empty_query = {
        "query": "",
        "user_id": "test_user_123"
    }

    response = client.post("/query", json=empty_query)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error response: {response.json()}")
    else:
        print(f"Unexpected success: {response.json()}")

    # Test scenario 2: Very long query (should fail validation)
    print("\n--- Test 2: Very long query ---")
    long_query = {
        "query": "This is a very long query " + "word " * 500,  # Over 1000 characters
        "user_id": "test_user_456"
    }

    response = client.post("/query", json=long_query)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error response: {response.json()}")
    else:
        print(f"Unexpected success: {response.json()}")

    # Test scenario 3: Query with SQL injection patterns (should fail validation)
    print("\n--- Test 3: Query with SQL injection pattern ---")
    injection_query = {
        "query": "What is the meaning of life? DROP TABLE users;",
        "user_id": "test_user_789"
    }

    response = client.post("/query", json=injection_query)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error response: {response.json()}")
    else:
        print(f"Response: {response.json()}")

    # Test scenario 4: Valid query (should succeed)
    print("\n--- Test 4: Valid query ---")
    valid_query = {
        "query": "What is a test?",
        "user_id": "test_user_001"
    }

    response = client.post("/query", json=valid_query)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: Answer preview: {data['answer'][:50]}...")
        print(f"Sources count: {len(data.get('sources', []))}")
    else:
        print(f"Unexpected error: {response.json()}")

    print("\n--- Error Handling Test Complete ---")

if __name__ == "__main__":
    test_error_handling()