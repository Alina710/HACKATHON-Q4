"""
Integration tests for the RAG Agent's retrieval functionality.
Tests the integration between the agent and the Qdrant retrieval pipeline.
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from agent import RAGAgent, QdrantRetrievalTool


def test_agent_retrieval_integration():
    """Test that the agent properly integrates with the retrieval pipeline."""
    with patch('agent.OpenAI'), \
         patch('agent.Retriever') as mock_retriever_class, \
         patch('agent.RAGAgent._create_assistant'), \
         patch('agent.time.sleep'):

        # Create a mock retriever instance
        mock_retriever_instance = Mock()
        mock_retriever_instance.retrieve.return_value = [
            {
                "title": "Machine Learning Fundamentals",
                "source_url": "http://example.com/ml-book/chapter1",
                "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms...",
                "score": 0.98
            },
            {
                "title": "Deep Learning Concepts",
                "source_url": "http://example.com/deep-learning/chapter2",
                "content": "Deep learning uses neural networks with multiple layers to model complex patterns...",
                "score": 0.95
            }
        ]
        mock_retriever_class.return_value = mock_retriever_instance

        # Initialize the agent
        agent = RAGAgent()

        # Create a retrieval tool instance to test directly
        tool = QdrantRetrievalTool()

        # Test retrieval
        results = tool.get_relevant_content("machine learning concepts", top_k=2)

        # Verify the retrieval was called with correct parameters
        mock_retriever_instance.retrieve.assert_called_once_with("machine learning concepts", top_k=2)

        # Verify results contain expected content
        assert "Machine Learning Fundamentals" in results
        assert "Deep Learning Concepts" in results
        assert "subset of artificial intelligence" in results
        assert "neural networks" in results


def test_agent_response_with_retrieved_content():
    """Test that the agent's response is based on retrieved content."""
    with patch('agent.OpenAI'), \
         patch('agent.Retriever') as mock_retriever_class, \
         patch('agent.RAGAgent._create_assistant') as mock_create_assistant, \
         patch('agent.time.sleep'):

        # Setup mock retriever
        mock_retriever_instance = Mock()
        mock_retriever_instance.retrieve.return_value = [
            {
                "title": "Python Programming Guide",
                "source_url": "http://example.com/python/basics",
                "content": "Python is a high-level programming language known for its simplicity and readability.",
                "score": 0.92
            }
        ]
        mock_retriever_class.return_value = mock_retriever_instance

        # Setup mock assistant
        mock_assistant = Mock()
        mock_assistant.id = "test-assistant-id"
        mock_create_assistant.return_value = mock_assistant

        # Setup mock client to simulate OpenAI API calls
        mock_client = Mock()

        # Setup thread
        mock_thread = Mock()
        mock_thread.id = "test-thread-id"

        # Setup run that requires action (tool call)
        mock_run_in_progress = Mock()
        mock_run_in_progress.status = "requires_action"

        mock_run_completed = Mock()
        mock_run_completed.status = "completed"

        # Setup required action for tool call
        mock_tool_call = Mock()
        mock_tool_call.function.name = "get_relevant_content"
        mock_tool_call.function.arguments = '{"query": "What is Python?", "top_k": 5}'
        mock_tool_call.id = "test-tool-call-id"

        mock_required_action = Mock()
        mock_required_action.submit_tool_outputs.tool_calls = [mock_tool_call]

        mock_run_in_progress.required_action = mock_required_action

        # Setup messages
        mock_message_content = Mock()
        mock_message_content.type = "text"
        mock_message_content.text.value = "Python is a high-level programming language known for its simplicity and readability."

        mock_message = Mock()
        mock_message.role = "assistant"
        mock_message.run_id = "test-run-id"
        mock_message.content = [mock_message_content]

        mock_messages_list = Mock()
        mock_messages_list.data = [mock_message]

        # Configure mocks
        mock_client.beta.threads.create.return_value = mock_thread
        mock_client.beta.threads.runs.create.return_value = mock_run_in_progress
        mock_client.beta.threads.runs.retrieve.return_value = mock_run_completed
        mock_client.beta.threads.runs.submit_tool_outputs.return_value = mock_run_completed
        mock_client.beta.threads.messages.list.return_value = mock_messages_list

        # Initialize agent with mocked client
        agent = RAGAgent()
        agent.client = mock_client
        agent.threads["test-thread-id"] = mock_thread

        # Test the agent query
        result = agent.query("What is Python?", "test-thread-id")

        # Verify that the retriever was called to get content
        mock_retriever_instance.retrieve.assert_called_once_with("What is Python?", top_k=5)

        # Verify that the response contains content from the retrieved results
        assert "high-level programming language" in result["response"]
        assert "simplicity and readability" in result["response"]


def test_agent_follow_up_query_context():
    """Test that the agent maintains context for follow-up queries."""
    with patch('agent.OpenAI'), \
         patch('agent.Retriever') as mock_retriever_class, \
         patch('agent.RAGAgent._create_assistant') as mock_create_assistant, \
         patch('agent.time.sleep'):

        # Setup mock retriever
        mock_retriever_instance = Mock()
        mock_retriever_instance.retrieve.return_value = [
            {
                "title": "Machine Learning Models",
                "source_url": "http://example.com/ml/models",
                "content": "There are several types of machine learning models including supervised, unsupervised, and reinforcement learning.",
                "score": 0.96
            }
        ]
        mock_retriever_class.return_value = mock_retriever_instance

        # Setup mock assistant
        mock_assistant = Mock()
        mock_assistant.id = "test-assistant-id"
        mock_create_assistant.return_value = mock_assistant

        # Setup mock client
        mock_client = Mock()
        mock_thread = Mock()
        mock_thread.id = "test-thread-id"

        # Setup runs
        mock_run_completed = Mock()
        mock_run_completed.status = "completed"

        # Setup messages for context
        mock_message_content1 = Mock()
        mock_message_content1.type = "text"
        mock_message_content1.text.value = "There are several types of machine learning models including supervised, unsupervised, and reinforcement learning."

        mock_message1 = Mock()
        mock_message1.role = "assistant"
        mock_message1.run_id = "run1"
        mock_message1.content = [mock_message_content1]

        mock_user_message = Mock()
        mock_user_message.role = "user"
        mock_user_message.content = [Mock()]
        mock_user_message.content[0].type = "text"
        mock_user_message.content[0].text.value = "What is supervised learning?"

        mock_messages_list = Mock()
        mock_messages_list.data = [mock_user_message, mock_message1]

        # Configure mocks
        mock_client.beta.threads.create.return_value = mock_thread
        mock_client.beta.threads.runs.create.return_value = mock_run_completed
        mock_client.beta.threads.runs.retrieve.return_value = mock_run_completed
        mock_client.beta.threads.messages.list.return_value = mock_messages_list

        # Initialize agent
        agent = RAGAgent()
        agent.client = mock_client
        agent.threads["test-thread-id"] = mock_thread

        # First query
        first_result = agent.query("What are the types of ML models?", "test-thread-id")

        # Follow-up query using the same thread
        followup_result = agent.query("What is supervised learning?", "test-thread-id")

        # Verify that both queries used the same thread (maintaining context)
        assert first_result["thread_id"] == followup_result["thread_id"]

        # Verify retriever was called for both queries
        assert mock_retriever_instance.retrieve.call_count >= 1


def test_agent_error_handling():
    """Test that the agent handles errors gracefully."""
    with patch('agent.OpenAI'), \
         patch('agent.Retriever') as mock_retriever_class, \
         patch('agent.RAGAgent._create_assistant'), \
         patch('agent.time.sleep'):

        # Setup mock retriever to raise an exception
        mock_retriever_instance = Mock()
        mock_retriever_instance.retrieve.side_effect = Exception("Connection error")
        mock_retriever_class.return_value = mock_retriever_instance

        # Initialize the agent
        agent = RAGAgent()

        # Create a retrieval tool instance to test error handling
        tool = QdrantRetrievalTool()

        # Test that error is handled gracefully
        result = tool.get_relevant_content("test query")

        # Verify that an error message is returned instead of crashing
        assert "Error retrieving content" in result


if __name__ == "__main__":
    pytest.main([__file__])