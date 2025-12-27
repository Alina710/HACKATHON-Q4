# AI Agent with Retrieval-Augmented Capabilities

This project implements an AI agent using the OpenAI Agents SDK that integrates with the existing Qdrant-based retrieval pipeline to answer questions about book content.

## Overview

The agent uses a custom retrieval tool to query Qdrant for relevant content chunks and responds based only on retrieved information, supporting simple follow-up queries through conversation context.

## Prerequisites

- Python 3.8+
- OpenAI API key
- Qdrant instance with book content indexed

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export QDRANT_URL="your-qdrant-url"
export QDRANT_API_KEY="your-qdrant-api-key"  # if authentication required
```

## Usage

### Interactive Mode
Run the agent in interactive mode:
```bash
python agent.py
```

This will start an interactive session where you can ask questions about the book content.

### Programmatic Usage
```python
from agent import RAGAgent

# Initialize the agent
agent = RAGAgent()

# Create a conversation thread
thread_id = agent.create_thread()

# Ask a question
result = agent.query("What are the key concepts in machine learning?", thread_id)
print(result["response"])

# Ask a follow-up question using the same thread for context
followup_result = agent.query("Can you elaborate on the second concept?", thread_id)
print(followup_result["response"])
```

## Architecture

The implementation consists of:

1. **QdrantRetrievalTool**: A wrapper around the existing Qdrant retrieval pipeline from `backend/retrieve.py`
2. **RAGAgent**: The main agent class that uses OpenAI's Assistant API
3. **Conversation Context**: Thread management for maintaining context across follow-up queries

## Testing

Run the unit tests:
```bash
python -m pytest tests/test_agent.py
```

Run the integration tests:
```bash
python -m pytest tests/integration/test_agent_retrieval.py
```

## Configuration

The agent can be configured with different parameters:

- `model`: OpenAI model to use (default: "gpt-4-turbo-preview")
- `top_k`: Number of results to retrieve (default: 5)

## Features

- **Retrieval-Augmented Generation**: Answers are generated based only on retrieved content
- **Context Management**: Follow-up queries maintain conversation context
- **Error Handling**: Graceful error handling for retrieval and API failures
- **Logging**: Comprehensive logging for debugging and monitoring