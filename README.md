# thoughtful.py

This is a sample providing a customer chat using pydantic-ai
using OpenAI or Anthropic APIs. Twenty to thirty minutes
isn't a lot of time to pull in a lot of extra fluff (eg., full stack,
RAG, etc.), so this is a simple example using pydantic-ai from the CLI.

You need either an OpenAI endpoint and credentials or Anthropic API key
to run.

## Install:

1. Clone
  ```bash
  git clone https://github.com/jketreno/thoughtful
  cd thoughtful
  ```

2. Run local
  ```bash
  pip install -r requirements.txt
  ```

3. Run via docker
  ```bash
  docker compose build
  docker run thoughtful
  ```

If using the container, the first time it runs it will install the
requirements into a volume bound ./venv directory so subsequent
runs won't need to re-install.

## Sample output:

```
$ docker compose run --remove-orphans thoughtful
[+] Creating 1/1
 ✔ Container thoughtful-thoughtful-run-03efcf092aa3  Removed                                 0.0s 
Container: python
Setting pip environment to /opt/python
Using Ollama with qwen2.5:7b for chat session at http://172.17.0.1:11434/v1.
Welcome to the Thoughtful AI chat session.
You can ask questions about Thoughtful AI's agents and their functionalities.
To end the session, just say done, or goodbye, etc.

> tell me about thoughtful
Thoughtful AI provides advanced AI solutions to enhance the efficiency of healthcare operations. Our suite includes automation agents like EVA, CAM, and PHIL that aim to streamline processes such as eligibility verification, claims processing, and payment posting.

Would you like more information on any specific agent or service?
> tell me about their claims processing
The claims processing agent (CAM) streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements.

If you have any specific questions about how CAM works or its benefits, feel free to ask!
> goodbye

So long, and thanks for all the fish.
```

## Configuring

See .env for configuration options. By default, the system
will use the OpenAI protocol to communicate with a local
Ollama server running on the same host.

If you have an ollama instance available, change `OPENAI_URL`
to point to that server.

The .env also supports using frontier models from OpenAI
and Anthropic.