# thoughtful.py
#
# This is a sample providing a customer chat using pydantic-ai
# using OpenAI, Ollama, or Anthropic's Claude. Twenty to thirty minutes
# isn't a lot of time to pull in a lot of extra fluff (eg., full stack,
# RAG, etc.), so this is a simple example using pydantic-ai from the CLI.
#
# See README.md for details on how to set up the environment.

from typing import TypedDict
from dotenv import load_dotenv
import json
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage
import os

# Predefiend Q&A; match the best question and provide the answer verbatim.
questions_str = """
[
  {
    "question": "What does the eligibility verification agent (EVA) do?",
    "answer": "EVA automates the process of verifying a patient’s eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
  },
  {
    "question": "What does the claims processing agent (CAM) do?",
    "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
  },
  {
    "question": "How does the payment posting agent (PHIL) work?",
    "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
  },
  {
    "question": "Tell me about Thoughtful AI's Agents.",
    "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
  },
  {
    "question": "What are the benefits of using Thoughtful AI's agents?",
    "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
  }
]
"""
# Parse the questions string into a JSON object to make sure the data was valid...
questions_json = json.loads(questions_str)

#
# The the context token length of all the questions is <300, so no need to build a similarity database using RAG.
# Just inject all the context into the system prompt.
#
system_prompt = f"""
You are a helpful AI agent that answers questions about Thoughtful AI.

Follow these guidelines:

- You must answer the question conversationally.
- You should retrieve the most relevant answer from a hardcoded set of responses about Thoughtful AI and provide that answer verbatim. Do not embellish or fabricate information.
- You should use the predefined dataset to answer the questions about Thoughtful AI and fallback to generic LLM responses for everything else.
- Do not make up answers or provide information that is not in the predefined dataset. Refer the customer to contact Thoughtful AI if you do not know the answer.
- If the question is not related to Thoughtful AI, you should respond with a generic answer or ask the user to clarify their question.
- If the user asks to exit, use the exit_chat tool to end the session.

{json.dumps(questions_json, indent=2)}
"""

# Keep secrets out of the code...
load_dotenv(override=True)

# Determine which LLM mode to use based on environment variable
llm_mode = os.getenv("LLM_MODE", "openai")

# Load either the OpanAIModel for Ollama or the AnthropicModel for Claude based on the LLM_MODE
# environment variable.
match llm_mode:
    case "openai":
        from pydantic_ai.models.openai import OpenAIModel
        from pydantic_ai.providers.openai import OpenAIProvider

        model_name = os.getenv("MODEL_NAME", "qwen2.5:7b")
        openai_api_key = os.getenv("OPENAI_API_KEY", "not-used")
        openai_url = os.getenv("OPENAI_URL", None)
        class ProviderConfig(TypedDict):
            api_key: str
            base_url: str | None
        provider_config : ProviderConfig = {
            "api_key": openai_api_key, 
            "base_url": openai_url
        }
        model = OpenAIModel(
            model_name=model_name,
            provider=OpenAIProvider(**provider_config),
        )
        print(
            f"Using Ollama with {model_name} for chat session"
            f"{f' at {openai_url}' if openai_url else ''}."
        )
    case "claude":
        from pydantic_ai.models.anthropic import AnthropicModel

        model_name = os.getenv("MODEL_NAME", "claude-3-5-haiku-latest")
        if os.getenv("ANTHROPIC_API_KEY") is None:
            raise ValueError("ANTHROPIC_API_KEY must be set in .env file for Claude mode")
        model = AnthropicModel(model_name)  # keep it cheap...
        print(f"Using Claude with {model_name} for chat session.")
    case _:
        raise ValueError(
            f"Unknown LLM_MODE: {llm_mode}. Supported modes are 'openai' and 'claude'. Please set the LLM_MODE environment variable accordingly."
        )


# Define the global application state
# This will be used to track whether the user wants to exit the chat session.
class AppState(BaseModel):
    done: bool = Field(default=False)


# Create the agent with the model and system prompt
agent = Agent(model, deps_type=AppState, system_prompt=system_prompt)


# Define the tool the LLM will call when the user wants to exit the chat session.
@agent.tool
def exit_chat(ctx: RunContext[AppState]):
    """If the user indicates they want to stop the chat session, quit, or exit, invoke this tool."""
    ctx.deps.done = True


async def main():
    # Initialize the application state; just tracking if 'done' is set by the exit_chat tool.
    app_state = AppState()
    # Track the message history for the chat session
    history: list[ModelMessage] = []
    print("Welcome to the Thoughtful AI chat session.")
    print("You can ask questions about Thoughtful AI's agents and their functionalities.")
    print("To end the session, just say done, or goodbye, etc.\n")
    # Run until app_state.done breaks out of the loop.
    while not app_state.done:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInterrupted. You could ask tell the chat you are done instead of using Ctrl-C.")
            break

        # If the user input is empty, continue to the next iteration
        if not user_input:
            continue

        # Run with streaming response
        async with agent.run_stream(user_input, message_history=history, deps=app_state) as result:
            async for text in result.stream_text(delta=True):
                print(text, end="", flush=True)
            print()
            history = result.all_messages()

    print("So long, and thanks for all the fish.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
