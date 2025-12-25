---
id: 1
title: Amend Constitution
stage: constitution
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: sp.constitution
labels: [constitution,documentation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
 You are an AI-native technical author and system architect operating under a strict specification-driven constitution.

Create a production-ready technical book and an embedded RAG chatbot using Claude Code, Spec-Kit Plus, Docusaurus, and GitHub Pages. Treat Spec-Kit Plus specs as the single source of truth. Write for developers with a CS background. Content must be accurate, clear, rigorous, and fully reproducible. Do not invent tools, APIs, or features.

Structure the book logically, with each chapter having a clear objective and a governing spec. Include only runnable, correct instructions and code.

Build and document an embedded RAG chatbot that answers questions about the full book and supports selected-text-only queries. In selected-text mode, use only the provided text. If the answer is missing, reply exactly: "The answer is not available in the provided text." Always reference the chapter or section used.

Use only this stack: OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdr
```

## Response snapshot

Updated the project constitution to align with the technical book and RAG chatbot project requirements. The new constitution includes principles for specification-driven development, reproducible content creation, stack compliance, developer-first documentation, quality assurance standards, and RAG chatbot accuracy. It defines the required technology stack and establishes governance processes.

## Outcome

- ✅ Impact: Updated constitution to guide technical book and RAG chatbot development
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Plan development of the technical book and RAG chatbot
- 🧠 Reflection: Constitution now properly aligned with project requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A