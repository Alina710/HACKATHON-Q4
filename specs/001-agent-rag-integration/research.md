# Research: AI Agent with Retrieval-Augmented Capabilities

## Overview
This research document outlines the findings and decisions made during the exploration of the existing codebase for implementing an AI agent with retrieval-augmented capabilities using the OpenAI Agents SDK and Qdrant.

## Decision: Integration with Existing Retrieval Pipeline
**Rationale**: The existing codebase has a well-established retrieval pipeline with Qdrant integration that includes:
- `QdrantRetriever` class in `backend/retrieve.py` with comprehensive search functionality
- `QdrantStorage` class in `book_ingestion/storage.py` for vector storage
- Cohere embedding integration for generating document and query embeddings
- Comprehensive validation in `validate_retrieval.py`

This existing pipeline provides all the necessary functionality for the agent's retrieval needs, so we will integrate directly with it rather than reimplementing retrieval logic.

**Alternatives considered**:
1. Building a new retrieval system from scratch - Rejected because it would duplicate existing functionality
2. Using a different vector database - Rejected because Qdrant is already well-integrated
3. Using a different embedding provider - Rejected because Cohere integration is already established

## Decision: Agent Architecture Pattern
**Rationale**: The agent will be implemented as a single `agent.py` file that:
- Initializes an OpenAI Assistant with custom tools
- Implements a retrieval tool that calls the existing Qdrant search functionality
- Uses OpenAI's thread management for conversation context
- Responds using only retrieved content chunks

This approach follows the specification requirement for a minimal implementation while leveraging the existing retrieval pipeline.

**Alternatives considered**:
1. Multi-file agent architecture - Rejected because the spec calls for a single agent.py file
2. Using OpenAI Functions instead of Tools - Rejected because Tools API is the recommended approach
3. Custom conversation management - Rejected because OpenAI's thread system handles context well

## Decision: Retrieval Tool Implementation
**Rationale**: The agent will use a custom tool that wraps the existing `QdrantRetriever.search()` method. This tool will:
- Accept a query string as input
- Call the existing retrieval pipeline
- Return relevant content chunks to the agent
- Allow the agent to compose responses based only on retrieved information

This approach ensures consistency with existing retrieval logic while providing the agent with access to book content.

**Alternatives considered**:
1. Direct Qdrant API calls from the agent - Rejected because it would duplicate existing validation logic
2. Separate microservice for retrieval - Rejected because it adds unnecessary complexity
3. Caching layer - Rejected because the existing pipeline is already efficient

## Technical Unknowns Resolved

### OpenAI SDK Integration
- **Issue**: No existing OpenAI integration in codebase
- **Resolution**: Will add `openai` package to requirements and implement agent using OpenAI Assistant API
- **Pattern**: Follow OpenAI's official documentation for Assistant API implementation

### Environment Configuration
- **Issue**: Agent needs access to Qdrant configuration
- **Resolution**: Will use same environment variables as existing pipeline (QDRANT_URL, QDRANT_API_KEY)
- **Pattern**: Follow existing configuration pattern in `backend/retrieve.py`

### Conversation Context
- **Issue**: How to handle follow-up queries as specified
- **Resolution**: Use OpenAI's Thread API to maintain conversation context
- **Pattern**: Each conversation will have its own thread ID to maintain context for up to 5 turns

## Implementation Strategy

### Phase 1: Basic Agent Setup
1. Create `agent.py` with OpenAI client initialization
2. Implement basic assistant creation with retrieval tool
3. Set up simple query-response cycle

### Phase 2: Retrieval Integration
1. Create wrapper function for existing retrieval pipeline
2. Integrate with OpenAI tools system
3. Test basic retrieval functionality

### Phase 3: Conversation Context
1. Implement thread management for follow-up queries
2. Test multi-turn conversations
3. Validate context preservation

## Risks and Mitigation

### Risk: Performance
- **Issue**: Agent responses might be slow due to retrieval overhead
- **Mitigation**: The existing pipeline is already optimized with batch processing and efficient search

### Risk: Accuracy
- **Issue**: Agent might generate responses not based on retrieved content
- **Mitigation**: Implement strict tool usage to ensure only retrieved content is used

### Risk: Qdrant Availability
- **Issue**: Agent might fail if Qdrant is unavailable
- **Mitigation**: Implement proper error handling with graceful degradation