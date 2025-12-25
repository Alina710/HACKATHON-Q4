<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Added sections: Technical Book Authoring, RAG Chatbot Development
Removed sections: None
Modified principles:
- Specification-Driven Development (from generic to book/RAG focused)
- Reproducible Content Creation (new principle)
- Stack Compliance (new principle)
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
Follow-up TODOs: None
-->

# Technical Book and RAG Chatbot Constitution

## Core Principles

### Specification-Driven Development
All content and functionality must be governed by Spec-Kit Plus specifications. Every chapter must have a clear objective and governing spec. No content or feature development without prior specification approval.

### Reproducible Content Creation
All instructions and code examples must be runnable and correct. Content must be accurate, clear, rigorous, and fully reproducible. No theoretical or untested examples allowed. Every code snippet must be verified in the target environment.

### Stack Compliance
Use only the approved technology stack: Claude Code, Spec-Kit Plus, Docusaurus, GitHub Pages, OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant. No additional tools, APIs, or features may be invented or introduced without explicit approval.

### Developer-First Documentation
Content must target developers with CS background. Technical depth and accuracy are paramount. All explanations must be comprehensive yet accessible to the target audience.

### Quality Assurance Standards
All content must meet production-ready standards. This includes: accurate technical information, runnable code examples, proper testing of all functionality, and comprehensive documentation of all features.

### RAG Chatbot Accuracy
The embedded RAG chatbot must provide precise answers referencing specific chapters or sections. When information is not available in the provided text, the chatbot must respond exactly with: "The answer is not available in the provided text."

## Technical Constraints

### Technology Stack Requirements
- Frontend: Docusaurus for documentation site
- Backend: FastAPI for API services
- Database: Neon Serverless Postgres for data persistence
- Vector Storage: Qdrant for RAG functionality
- AI Integration: OpenAI Agents/ChatKit SDKs for chatbot
- Documentation: Spec-Kit Plus specs as single source of truth
- Hosting: GitHub Pages for static content

### Content Standards
- Chapters must have clear objectives and measurable outcomes
- All code examples must be complete, tested, and include expected output
- Technical accuracy must be verified by subject matter experts
- Content must be structured logically with progressive complexity

## Development Workflow

### Specification Process
1. All chapters require a governing spec before content creation
2. Specs must include clear objectives, acceptance criteria, and test cases
3. Content must strictly adhere to its governing specification
4. Changes to specs require formal approval process

### Review and Quality Gates
- Technical accuracy review by subject matter experts
- Code example verification and testing
- Cross-reference validation for RAG chatbot responses
- Accessibility and usability testing for documentation site

## Governance

Specifications from Spec-Kit Plus serve as the single source of truth for all development. All PRs and reviews must verify compliance with governing specifications. Complexity must be justified with clear benefits to the end user. Use this constitution for development guidance and decision-making.

**Version**: 1.1.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2025-12-23
