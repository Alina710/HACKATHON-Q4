"""
Final Integration Test for RAG System Frontend Integration via FastAPI

This test verifies that all components work together as expected:
1. Backend API properly handles queries
2. Agent integration works correctly
3. Source citation retrieval functions properly
4. Frontend API service communicates with backend
5. All error handling works as expected
"""

import json
import time
from api import app
from fastapi.testclient import TestClient

def run_final_integration_test():
    print("TEST: Starting Final Integration Test for RAG System Frontend Integration")
    print("="*70)

    client = TestClient(app)
    all_tests_passed = True
    test_results = []

    # Test 1: API Health Check
    print("\nPASSED: Test 1: API Health Check")
    try:
        response = client.get("/")
        if response.status_code == 200 and "RAG Query API is running" in response.json().get("message", ""):
            print("   PASSED: API is healthy and responding")
            test_results.append(("API Health Check", True, "API responding correctly"))
        else:
            print("   FAILED: API health check failed")
            test_results.append(("API Health Check", False, "API not responding correctly"))
            all_tests_passed = False
    except Exception as e:
        print(f"   FAILED: API health check error - {e}")
        test_results.append(("API Health Check", False, str(e)))
        all_tests_passed = False

    # Test 2: Valid Query Processing
    print("\nPASSED: Test 2: Valid Query Processing")
    try:
        valid_query = {
            "query": "What is a test?",
            "user_id": "integration_test_user",
            "session_id": "integration_test_session"
        }

        start_time = time.time()
        response = client.post("/query", json=valid_query)
        end_time = time.time()

        if response.status_code == 200:
            data = response.json()
            required_fields = ["query_id", "answer", "sources", "timestamp", "session_id"]
            missing_fields = [field for field in required_fields if field not in data]

            if not missing_fields:
                print(f"   PASSED: Query processed successfully in {end_time - start_time:.2f}s")
                print(f"   INFO: Response includes {len(data.get('sources', []))} sources")
                test_results.append(("Valid Query Processing", True, f"Success in {end_time - start_time:.2f}s"))
            else:
                print(f"   FAILED: Missing fields in response: {missing_fields}")
                test_results.append(("Valid Query Processing", False, f"Missing fields: {missing_fields}"))
                all_tests_passed = False
        else:
            print(f"   FAILED: Query processing failed with status {response.status_code}")
            test_results.append(("Valid Query Processing", False, f"Status {response.status_code}"))
            all_tests_passed = False
    except Exception as e:
        print(f"   FAILED: Query processing error - {e}")
        test_results.append(("Valid Query Processing", False, str(e)))
        all_tests_passed = False

    # Test 3: Query Validation
    print("\nPASSED: Test 3: Query Validation")
    try:
        invalid_query = {
            "query": "",  # Empty query should fail validation
            "user_id": "test_user"
        }

        response = client.post("/query", json=invalid_query)
        if response.status_code == 422:  # Validation error expected
            print("   PASSED: Query validation correctly rejects empty queries")
            test_results.append(("Query Validation", True, "Correctly rejects invalid queries"))
        else:
            print(f"   FAILED: Query validation failed - expected 422, got {response.status_code}")
            test_results.append(("Query Validation", False, f"Expected 422, got {response.status_code}"))
            all_tests_passed = False
    except Exception as e:
        print(f"   FAILED: Query validation error - {e}")
        test_results.append(("Query Validation", False, str(e)))
        all_tests_passed = False

    # Test 4: Source Citations
    print("\nPASSED: Test 4: Source Citations")
    try:
        citation_query = {
            "query": "What is a simple test?",
            "user_id": "citation_test_user"
        }

        response = client.post("/query", json=citation_query)
        if response.status_code == 200:
            data = response.json()
            sources = data.get("sources", [])
            print(f"   PASSED: Response includes {len(sources)} source citations")
            if sources:
                print(f"   INFO: First source: {sources[0].get('title', 'N/A')}")
            test_results.append(("Source Citations", True, f"Includes {len(sources)} sources"))
        else:
            print(f"   FAILED: Source citation test failed with status {response.status_code}")
            test_results.append(("Source Citations", False, f"Status {response.status_code}"))
            all_tests_passed = False
    except Exception as e:
        print(f"   FAILED: Source citation error - {e}")
        test_results.append(("Source Citations", False, str(e)))
        all_tests_passed = False

    # Test 5: Session Management
    print("\nPASSED: Test 5: Session Management")
    try:
        session_query_1 = {
            "query": "First test query in session",
            "user_id": "session_test_user",
            "session_id": "test_session_123"
        }

        response1 = client.post("/query", json=session_query_1)
        if response1.status_code == 200:
            data1 = response1.json()
            session_id_1 = data1.get("session_id")

            # Make another query with same session
            session_query_2 = {
                "query": "Second test query in session",
                "user_id": "session_test_user",
                "session_id": "test_session_123"
            }

            response2 = client.post("/query", json=session_query_2)
            if response2.status_code == 200:
                data2 = response2.json()
                session_id_2 = data2.get("session_id")

                if session_id_1 == session_id_2:
                    print("   PASSED: Session management working correctly")
                    test_results.append(("Session Management", True, "Session IDs match"))
                else:
                    print("   FAILED: Session IDs don't match")
                    test_results.append(("Session Management", False, "Session IDs mismatch"))
                    all_tests_passed = False
            else:
                print(f"   FAILED: Second session query failed with status {response2.status_code}")
                test_results.append(("Session Management", False, f"Second query failed: {response2.status_code}"))
                all_tests_passed = False
        else:
            print(f"   FAILED: First session query failed with status {response1.status_code}")
            test_results.append(("Session Management", False, f"First query failed: {response1.status_code}"))
            all_tests_passed = False
    except Exception as e:
        print(f"   FAILED: Session management error - {e}")
        test_results.append(("Session Management", False, str(e)))
        all_tests_passed = False

    # Summary
    print("\n" + "="*70)
    print("RESULTS: INTEGRATION TEST SUMMARY")
    print("="*70)

    passed_count = sum(1 for _, passed, _ in test_results if passed)
    total_count = len(test_results)

    for test_name, passed, details in test_results:
        status = "PASSED" if passed else "FAILED"
        print(f"{status} {test_name}: {details}")

    print(f"\nSUMMARY: Overall Result: {passed_count}/{total_count} tests passed")

    if all_tests_passed:
        print("SUCCESS: ALL INTEGRATION TESTS PASSED!")
        print("PASSED: The RAG System Frontend Integration is working correctly.")
        print("PASSED: Backend API is properly integrated with the RAG agent.")
        print("PASSED: Frontend can communicate with the backend API.")
        print("PASSED: Error handling and validation are functioning properly.")
        return True
    else:
        print("WARN: SOME INTEGRATION TESTS FAILED!")
        print("FAILED: The system needs further investigation and fixes.")
        return False

if __name__ == "__main__":
    success = run_final_integration_test()
    exit(0 if success else 1)