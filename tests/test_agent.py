"""
Tests for the RAG Agent functionality.
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from agent import RAGAgent, QdrantRetrievalTool


def test_qdrant_retrieval_tool_initialization():
    """Test that QdrantRetrievalTool initializes correctly."""
    with patch('agent.Retriever') as mock_retriever_class:
        mock_retriever_instance = Mock()
        mock_retriever_class.return_value = mock_retriever_instance

        tool = QdrantRetrievalTool()

        assert tool.retriever == mock_retriever_instance
        mock_retriever_class.assert_called_once()


def test_qdrant_retrieval_tool_get_relevant_content():
    """Test that the retrieval tool can get relevant content."""
    with patch('agent.Retriever') as mock_retriever_class:
        mock_retriever_instance = Mock()
        mock_retriever_instance.retrieve.return_value = [
            {
                "title": "Test Title",
                "source_url": "http://test.com",
                "content": "Test content for retrieval",
                "score": 0.95
            }
        ]
        mock_retriever_class.return_value = mock_retriever_instance

        tool = QdrantRetrievalTool()
        result = tool.get_relevant_content("test query", top_k=1)

        assert "Test Title" in result
        assert "http://test.com" in result
        assert "Test content for retrieval" in result
        mock_retriever_instance.retrieve.assert_called_once_with("test query", top_k=1)


def test_rag_agent_initialization():
    """Test that RAGAgent initializes correctly."""
    with patch('agent.OpenAI'), \
         patch('agent.Retriever'), \
         patch('agent.RAGAgent._create_assistant') as mock_create_assistant:

        mock_assistant = Mock()
        mock_assistant.id = "test-assistant-id"
        mock_create_assistant.return_value = mock_assistant

        agent = RAGAgent(model="gpt-4-test")

        assert agent.model == "gpt-4-test"
        assert isinstance(agent.retrieval_tool, QdrantRetrievalTool)
        mock_create_assistant.assert_called_once()


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_rag_agent_create_thread():
    """Test that RAGAgent can create a thread."""
    with patch('agent.OpenAI'), \
         patch('agent.Retriever'), \
         patch('agent.RAGAgent._create_assistant'), \
         patch('agent.time.sleep'):  # Mock time.sleep to avoid actual delays

        mock_client = Mock()
        mock_thread = Mock()
        mock_thread.id = "test-thread-id"
        mock_client.beta.threads.create.return_value = mock_thread

        agent = RAGAgent()
        agent.client = mock_client

        thread_id = agent.create_thread()

        assert thread_id == "test-thread-id"
        mock_client.beta.threads.create.assert_called_once()


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_rag_agent_query():
    """Test that RAGAgent can process a query."""
    with patch('agent.OpenAI'), \
         patch('agent.Retriever'), \
         patch('agent.RAGAgent._create_assistant'), \
         patch('agent.time.sleep'):  # Mock time.sleep to avoid actual delays

        # Setup mock client
        mock_client = Mock()

        # Setup thread
        mock_thread = Mock()
        mock_thread.id = "test-thread-id"

        # Setup run
        mock_run = Mock()
        mock_run.id = "test-run-id"
        mock_run.status = "completed"

        # Setup message
        mock_message_content = Mock()
        mock_message_content.type = "text"
        mock_message_content.text.value = "Test response from agent"

        mock_message = Mock()
        mock_message.role = "assistant"
        mock_message.run_id = "test-run-id"
        mock_message.content = [mock_message_content]

        # Setup messages list
        mock_messages_list = Mock()
        mock_messages_list.data = [mock_message]

        # Configure mocks
        mock_client.beta.threads.create.return_value = mock_thread
        mock_client.beta.threads.runs.create.return_value = mock_run
        mock_client.beta.threads.runs.retrieve.return_value = mock_run
        mock_client.beta.threads.messages.list.return_value = mock_messages_list

        agent = RAGAgent()
        agent.client = mock_client
        agent.threads["test-thread-id"] = mock_thread

        result = agent.query("test query", "test-thread-id")

        assert result["response"] == "Test response from agent"
        assert result["thread_id"] == "test-thread-id"
        assert result["status"] == "success"


if __name__ == "__main__":
    pytest.main([__file__])