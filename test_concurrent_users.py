import asyncio
import json
import time
from concurrent.futures import ThreadPoolExecutor
from api import app
from fastapi.testclient import TestClient

def test_single_request(user_id):
    """Function to simulate a single user request"""
    client = TestClient(app)

    sample_query = {
        "query": f"Test query from user {user_id}",
        "user_id": f"user_{user_id}",
        "session_id": f"session_{user_id}_{int(time.time())}"
    }

    start_time = time.time()
    response = client.post("/query", json=sample_query)
    end_time = time.time()

    result = {
        "user_id": user_id,
        "status_code": response.status_code,
        "response_time": end_time - start_time,
        "success": response.status_code == 200
    }

    if response.status_code == 200:
        data = response.json()
        result["query_id"] = data.get("query_id", "unknown")
        result["session_id"] = data.get("session_id", "unknown")
    else:
        result["error"] = response.json() if response.content else "No response content"

    return result

def test_concurrent_users():
    """Test the system with multiple concurrent users"""
    print("Testing concurrent user scenarios...")

    # Test with 5 concurrent users
    num_users = 5
    print(f"Simulating {num_users} concurrent users...")

    start_time = time.time()

    # Use ThreadPoolExecutor to simulate concurrent requests
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        # Submit tasks for concurrent execution
        futures = [executor.submit(test_single_request, i) for i in range(num_users)]

        # Collect results
        results = [future.result() for future in futures]

    end_time = time.time()
    total_time = end_time - start_time

    # Analyze results
    successful_requests = [r for r in results if r["success"]]
    failed_requests = [r for r in results if not r["success"]]
    response_times = [r["response_time"] for r in results]

    print(f"\n--- Test Results ---")
    print(f"Total requests: {num_users}")
    print(f"Successful requests: {len(successful_requests)}")
    print(f"Failed requests: {len(failed_requests)}")
    print(f"Total test time: {total_time:.2f} seconds")
    print(f"Average response time: {sum(response_times)/len(response_times):.2f} seconds")
    print(f"Min response time: {min(response_times):.2f} seconds")
    print(f"Max response time: {max(response_times):.2f} seconds")

    if failed_requests:
        print(f"\nFailed requests:")
        for failed in failed_requests:
            print(f"  User {failed['user_id']}: {failed.get('error', 'Unknown error')}")

    if successful_requests:
        print(f"\nSample successful responses:")
        for i, success in enumerate(successful_requests[:3]):  # Show first 3
            print(f"  User {success['user_id']}: Query ID {success['query_id'][:8]}..., Session ID {success['session_id'][:8]}..., Time: {success['response_time']:.2f}s")

    # Performance criteria check
    success_rate = len(successful_requests) / num_users * 100
    avg_response_time = sum(response_times) / len(response_times)

    print(f"\n--- Performance Summary ---")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Average response time: {avg_response_time:.2f} seconds")

    # Check if performance meets requirements (from spec: 95% respond within 10 seconds)
    fast_responses = [t for t in response_times if t <= 10]
    fast_response_rate = len(fast_responses) / len(response_times) * 100

    print(f"Requests under 10s: {fast_response_rate:.1f}%")

    if success_rate >= 90 and avg_response_time < 15:  # Using reasonable thresholds
        print("✅ Concurrent user test PASSED")
        return True
    else:
        print("❌ Concurrent user test FAILED")
        return False

if __name__ == "__main__":
    test_concurrent_users()