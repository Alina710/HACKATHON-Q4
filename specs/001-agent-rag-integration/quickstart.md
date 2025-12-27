# Quickstart: AI Agent with Retrieval-Augmented Capabilities

## Overview
This guide provides a quick start for implementing and using the AI agent with retrieval-augmented capabilities using the OpenAI Agents SDK and Qdrant.

## Prerequisites

### Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install OpenAI dependencies
pip install openai
```

### Environment Variables
Set up the required environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export QDRANT_URL="your-qdrant-url"
export QDRANT_API_KEY="your-qdrant-api-key"  # if authentication required
```

### Data Preparation
Ensure book content is already ingested into Qdrant:
1. Run the book ingestion pipeline to populate Qdrant with content
2. Verify that the "book_embeddings" collection exists in Qdrant
3. Test retrieval functionality using `validate_retrieval.py`

## Installation

### Update Requirements
Add the OpenAI dependency to your `requirements.txt`:
```
openai>=1.0.0
```

### Single File Implementation
The agent is implemented in a single file as specified:
- `agent.py` - Contains the complete agent implementation

## Basic Usage

### Initialize the Agent
```python
from agent import BookContentAgent

# Initialize the agent
agent = BookContentAgent()

# Or initialize with specific configuration
agent = BookContentAgent(
    openai_api_key="your-openai-api-key",
    qdrant_url="your-qdrant-url",
    qdrant_api_key="your-qdrant-api-key"
)
```

### Create a Session and Ask Questions
```python
# Create a new session
session = agent.create_session()

# Ask a question about book content
response = agent.ask_question(
    session_id=session.session_id,
    query="What are the key concepts in chapter 3?"
)

print(response.response_text)
```

### Handle Follow-up Queries
```python
# The agent maintains context for follow-up queries
followup_response = agent.ask_question(
    session_id=session.session_id,
    query="Can you elaborate on the second concept you mentioned?"
)

print(followup_response.response_text)
```

## Advanced Usage

### Direct Tool Access
Access the retrieval tool directly:
```python
# Retrieve content chunks directly
chunks = agent.retrieve_content("query about book content")
for chunk in chunks:
    print(f"Source: {chunk.source_url}")
    print(f"Content: {chunk.content[:200]}...")
```

### Session Management
```python
# List active sessions
active_sessions = agent.list_sessions()

# End a session
agent.end_session(session.session_id)

# Check session status
status = agent.get_session_status(session.session_id)
```

## Testing

### Run Unit Tests
```bash
# Run agent-specific tests
python -m pytest tests/test_agent.py

# Run integration tests
python -m pytest tests/integration/test_agent_retrieval.py
```

### Validate Retrieval
Test that the agent can properly retrieve content:
```bash
python -c "
from agent import BookContentAgent
agent = BookContentAgent()
session = agent.create_session()
response = agent.ask_question(session.session_id, 'Test query')
print('Agent response:', response.response_text)
"
```

## Troubleshooting

### Common Issues

#### Qdrant Connection Issues
- Verify QDRANT_URL and QDRANT_API_KEY are correctly set
- Check that the Qdrant server is running and accessible
- Ensure the "book_embeddings" collection exists

#### OpenAI API Issues
- Verify OPENAI_API_KEY is correctly set
- Check that your OpenAI account has sufficient credits
- Verify that the Assistant API is enabled for your account

#### Empty Retrieval Results
- Confirm that book content has been ingested into Qdrant
- Check that the ingestion pipeline completed successfully
- Verify that queries match the content in your documents

## Configuration

### Agent Parameters
The agent can be configured with the following parameters:
- `model`: OpenAI model to use (default: gpt-4-turbo)
- `retrieval_limit`: Maximum number of chunks to retrieve (default: 5)
- `context_window`: Maximum conversation turns to maintain (default: 5)
- `temperature`: Response creativity parameter (default: 0.3)

### Environment Variables Reference
- `OPENAI_API_KEY`: API key for OpenAI services
- `QDRANT_URL`: URL for Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant authentication (if required)
- `QDRANT_COLLECTION`: Name of the collection to query (default: book_embeddings)

## Next Steps

1. **Customization**: Modify the agent's system prompt to match your specific book content
2. **Evaluation**: Test the agent with various question types to ensure accuracy
3. **Integration**: Connect the agent to your application's user interface
4. **Monitoring**: Implement logging and monitoring for production use