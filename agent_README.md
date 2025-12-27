# AI Agent with Retrieval-Augmented Generation

This project implements an AI agent with retrieval-augmented generation (RAG) capabilities using the OpenAI Agents SDK and Qdrant vector database.

## Overview

The agent uses the OpenAI Agents SDK with a custom retrieval tool that queries Qdrant for relevant book content chunks. This enables the agent to answer questions based on retrieved information rather than relying solely on its pre-trained knowledge.

## Features

- OpenAI Agents SDK with custom retrieval tool
- Integration with existing Qdrant retrieval pipeline
- Source citation in responses
- Simplified agent orchestration

## Requirements

- Python 3.8+
- OpenAI API key
- Qdrant vector database with ingested content
- Cohere API key (for embeddings)

## Setup

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Create a `.env` file with the following environment variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   ```

3. Ensure you have ingested content in your Qdrant collection named "documents"

## Usage

Run the agent interactively:

```bash
python agent.py
```

The agent will:
1. Create an OpenAI Agent with retrieval capabilities
2. Allow you to ask questions about the book content
3. Use the retrieval tool to find relevant information from Qdrant
4. Cite sources from the retrieved content

## Architecture

- `RAGAgent`: Main class that manages the OpenAI Agent
- `get_relevant_content`: Custom function tool that queries Qdrant
- Integration with existing `backend/retrieve.py` pipeline
- Using OpenAI Agents SDK for simplified orchestration

## Testing

Run the unit tests:
```bash
python test_agent_sdk.py
```