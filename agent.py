#!/usr/bin/env python3
"""
AI Agent with Retrieval-Augmented Generation capabilities.
Uses OpenRouter (instead of OpenAI billing) + Qdrant retrieval.
"""

import os
import logging
from typing import Dict, Any

from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from openai import AsyncOpenAI

from backend.retrieve import Retriever

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1"
)

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file. Please set the OPENROUTER_API_KEY environment variable.")

# --------------------------------------------------
# Initialize OpenRouter client
# --------------------------------------------------
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)

# --------------------------------------------------
# Logging setup
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Retrieval logic
# --------------------------------------------------
def _get_relevant_content_impl(query: str, top_k: int = 5) -> str:
    try:
        retriever = Retriever()
        logger.info(f"Retrieving content for query: {query}")

        results = retriever.retrieve(query, top_k=top_k)

        if not results:
            return "No relevant content found in the knowledge base."

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"Result {i}:\n"
                f"Title: {r.get('title', 'N/A')}\n"
                f"Source: {r.get('source_url', 'N/A')}\n"
                f"Score: {r.get('score', 0):.4f}\n"
                f"Content: {r.get('content', '')[:600]}...\n"
            )

        return "\n".join(formatted)

    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        return "Error occurred while retrieving content."

# --------------------------------------------------
# Tool for the Agent
# --------------------------------------------------
@function_tool
def get_relevant_content(query: str, top_k: int = 5) -> str:
    return _get_relevant_content_impl(query, top_k)

# --------------------------------------------------
# RAG Agent
# --------------------------------------------------
class RAGAgent:
    def __init__(self, model: str = "mistralai/mistral-7b-instruct"):
        self.model_name = model
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        from agents import OpenAIChatCompletionsModel
        # Create a custom model with the OpenRouter client
        custom_model = OpenAIChatCompletionsModel(
            model=self.model_name,
            openai_client=client  # Use the global OpenRouter client
        )

        agent = Agent(
            name="RAG Book Assistant",
            model=custom_model,
            instructions=(
                "You are a RAG-based assistant. "
                "Always use the get_relevant_content tool before answering. "
                "Answer ONLY from retrieved content. "
                "If the answer is not present, clearly say so. "
                "Always mention sources."
            ),
            tools=[get_relevant_content],
        )

        logger.info("RAG Agent created successfully")
        return agent

    def query(self, user_message: str) -> Dict[str, Any]:
        logger.info(f"User query: {user_message}")
        try:
            result = Runner.run_sync(self.agent, user_message)
            return {
                "status": "success",
                "response": result.final_output
            }
        except Exception as e:
            logger.error(f"Agent error: {e}")
            return {
                "status": "error",
                "response": "LLM response failed, but retrieval works correctly."
            }

# --------------------------------------------------
# Main loop
# --------------------------------------------------
def main():
    logger.info("Initializing RAG Agent...")
    agent = RAGAgent()

    print("\nRAG Agent ready (OpenRouter enabled)")
    print("Type 'quit' to exit")
    print("-" * 50)

    while True:
        try:
            query = input("\nYour question: ").strip()

            if query.lower() == "quit":
                print("Goodbye!")
                break

            if not query:
                continue

            result = agent.query(query)
            print("\nAgent response:\n")
            print(result["response"])

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(e)
            print("Unexpected error occurred.")

# --------------------------------------------------
if __name__ == "__main__":
    main()
    