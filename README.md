# thoughtful.py

This is a sample providing a customer chat using pydantic-ai
using OpenAI or Anthropic APIs. Twenty to thirty minutes
isn't a lot of time to pull in a lot of extra fluff (eg., full stack,
RAG, etc.), so this is a simple example using pydantic-ai from the CLI.

You need either an OpenAI endpoint and credentials or Anthropic API key
to run.

## Install:

```bash
git clone https://github.com/jketreno/thoughtful
cd thoughtful
pip install pydantic-ai[openai,anthropic]
```

## Usage:
```bash
LLM_MODE=claude python thoughtful.py
```

In your .env (or exported in environment), provide the following variables:

```.env
LLM_MODE=openai
# LLM_MODE=claude
MODEL_NAME=qwen2.5:7b
# MODEL_NAME=claude-3-5-haiku-latest
# If using Claude, set ANTHROPIC_API_KEY:
#ANTHROPIC_API_KEY=your_anthropic_api_key
# If using OpenAI, set OPENAI_API_KEY:
# OPENAI_API_KEY=your_openai_key
# If using self hosted Ollama, set OPENAI_URL to your Ollama server URL:
OPENAI_URL=http://ollama:11434/v1
```
