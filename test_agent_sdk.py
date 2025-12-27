#!/usr/bin/env python3
"""
Simple test script for the RAG Agent using OpenAI Agents SDK.
This tests the basic functionality without requiring full API keys.
"""

import os
from unittest.mock import Mock, patch
from agent import RAGAgent, _get_relevant_content_impl

def test_agent_creation():
    """Test that the agent can be created without errors."""
    print("Testing agent creation...")

    # Mock the Agent and Runner to avoid API calls during testing
    with patch('agent.Agent') as mock_agent_class, \
         patch('agent.Runner') as mock_runner_class, \
         patch('agent.Retriever') as mock_retriever_class:

        # Set up mocks
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance

        mock_result = Mock()
        mock_result.final_output = "Test response"
        mock_runner_class.run_sync.return_value = mock_result

        mock_retriever_instance = Mock()
        mock_retriever_instance.retrieve.return_value = [
            {
                'content': 'This is test content',
                'source_url': 'https://test.com',
                'title': 'Test Title',
                'score': 0.9
            }
        ]
        mock_retriever_class.return_value = mock_retriever_instance

        # Create the agent
        agent = RAGAgent()

        # Verify the agent was created
        mock_agent_class.assert_called_once()
        print("OK - Agent creation successful")

def test_retrieval_tool():
    """Test the retrieval tool functionality."""
    print("Testing retrieval tool...")

    # Mock the retriever
    with patch('agent.Retriever') as mock_retriever_class:
        mock_retriever_instance = Mock()
        mock_retriever_instance.retrieve.return_value = [
            {
                'content': 'This is test content',
                'source_url': 'https://test.com',
                'title': 'Test Title',
                'score': 0.9
            }
        ]
        mock_retriever_class.return_value = mock_retriever_instance

        # Test the retrieval function
        result = _get_relevant_content_impl("test query")

        # Verify the retriever was called
        mock_retriever_instance.retrieve.assert_called_once_with("test query", top_k=5)

        # Check that the result contains the expected content
        assert "This is test content" in result
        print("OK - Retrieval tool test successful")

def test_agent_query():
    """Test agent query functionality."""
    print("Testing agent query...")

    with patch('agent.Agent') as mock_agent_class, \
         patch('agent.Runner') as mock_runner_class, \
         patch('agent.Retriever') as mock_retriever_class:

        # Set up mocks
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance

        mock_result = Mock()
        mock_result.final_output = "This is a test response from the agent."
        mock_runner_class.run_sync.return_value = mock_result

        mock_retriever_instance = Mock()
        mock_retriever_instance.retrieve.return_value = [
            {
                'content': 'Test content for query',
                'source_url': 'https://test.com',
                'title': 'Test Title',
                'score': 0.85
            }
        ]
        mock_retriever_class.return_value = mock_retriever_instance

        # Create the agent
        agent = RAGAgent()

        # Test the query method
        result = agent.query("What is test?")

        # Verify the runner was called
        mock_runner_class.run_sync.assert_called_once()

        # Check the result
        assert result['status'] == 'success'
        assert 'test response' in result['response'].lower()
        print("OK - Agent query test successful")

if __name__ == "__main__":
    print("Running RAG Agent tests with OpenAI Agents SDK...\n")

    try:
        test_agent_creation()
        test_retrieval_tool()
        test_agent_query()

        print("\nOK - All tests passed successfully!")
        print("\nNote: These tests use mocked API calls.")
        print("To run the full agent, you'll need valid API keys in a .env file.")

    except Exception as e:
        print(f"\nFAILED - Test failed with error: {e}")
        raise