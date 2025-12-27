#!/usr/bin/env python3
"""
Simple test script for the RAG Agent.
This tests the basic functionality without requiring full API keys.
"""

import os
from unittest.mock import Mock, patch
from agent import RAGAgent, QdrantRetrievalTool

def test_agent_creation():
    """Test that the agent can be created without errors."""
    print("Testing agent creation...")

    # Mock both OpenAI client and the backend retriever to avoid API calls during testing
    with patch('agent.OpenAI') as mock_openai, \
         patch('agent.Retriever') as mock_retriever_class:

        mock_client = Mock()
        mock_openai.return_value = mock_client

        # Set up mock assistant
        mock_assistant = Mock()
        mock_assistant.id = "test-assistant-id"
        mock_client.beta.assistants.create.return_value = mock_assistant

        # Mock the retriever
        mock_retriever_instance = Mock()
        mock_retriever_class.return_value = mock_retriever_instance

        # Create the agent
        agent = RAGAgent()

        # Verify the assistant was created
        mock_client.beta.assistants.create.assert_called_once()
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

        # Create the retrieval tool
        tool = QdrantRetrievalTool()

        # Test the retrieval method
        result = tool.get_relevant_content("test query")

        # Verify the retriever was called
        mock_retriever_instance.retrieve.assert_called_once_with("test query", top_k=5)

        # Check that the result contains the expected content
        assert "This is test content" in result
        print("OK - Retrieval tool test successful")

def test_thread_creation():
    """Test thread creation functionality."""
    print("Testing thread creation...")

    with patch('agent.OpenAI') as mock_openai, \
         patch('agent.Retriever') as mock_retriever_class:

        mock_client = Mock()
        mock_openai.return_value = mock_client

        # Set up mock assistant and thread
        mock_assistant = Mock()
        mock_assistant.id = "test-assistant-id"
        mock_thread = Mock()
        mock_thread.id = "test-thread-id"

        mock_client.beta.assistants.create.return_value = mock_assistant
        mock_client.beta.threads.create.return_value = mock_thread

        # Mock the retriever
        mock_retriever_instance = Mock()
        mock_retriever_class.return_value = mock_retriever_instance

        # Create the agent
        agent = RAGAgent()

        # Create a thread
        thread_id = agent.create_thread()

        # Verify thread was created
        mock_client.beta.threads.create.assert_called_once()
        assert thread_id == "test-thread-id"
        print("OK - Thread creation test successful")

if __name__ == "__main__":
    print("Running RAG Agent tests...\n")

    try:
        test_agent_creation()
        test_retrieval_tool()
        test_thread_creation()

        print("\nOK - All tests passed successfully!")
        print("\nNote: These tests use mocked API calls.")
        print("To run the full agent, you'll need valid API keys in a .env file.")

    except Exception as e:
        print(f"\nFAILED - Test failed with error: {e}")
        raise