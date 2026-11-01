# Architecture

## Current implementation

This repository currently provides a small HTTP API for text conversations with
an OpenAI-compatible chat-completions provider. It is a foundation, not yet a
general-purpose autonomous agent.

```text
HTTP client
    |
    v
FastAPI application (src/personal_ai_agent/app.py)
    |-- GET / (browser chat interface)
    |-- GET /health
    |-- POST /chat
    |       |
    |       +-- request validation (Pydantic)
    |       +-- up to 20 prior user/assistant messages supplied by the browser
    |       +-- LLM client (src/personal_ai_agent/llm.py)
    |               |
    |               +-- configured chat-completions HTTP endpoint
    |
    +-- browser interface (src/personal_ai_agent/static/index.html)
    |
    +-- settings loaded from environment (src/personal_ai_agent/config.py)
```

## Request flow

1. `GET /` serves the browser-based chat interface. `GET /health` is available
   for service checks.
2. `POST /chat` accepts a non-empty `message` of at most 10,000 characters and
   up to 20 validated prior user/assistant messages.
3. FastAPI validates the request. Invalid input receives HTTP 422.
4. The application checks that `OPENAI_API_KEY` is configured. If it is not,
   the request receives HTTP 503; health checks remain available.
5. The LLM client sends the supplied conversation and new user message to
   `{OPENAI_BASE_URL}/chat/completions`, using the configured model and timeout.
6. A valid provider response is returned as `{"reply": "..."}`. Provider
   timeouts return HTTP 504; provider/network errors or malformed responses
   return HTTP 502. Error responses do not include provider bodies or secrets.
7. Conversation history is held only in the browser page and sent with each
   request; it is not persisted by the service.

## Components and boundaries

- **API (`app.py`, `src/personal_ai_agent/app.py`)**: ASGI entry point, browser
  route, chat and health routes, request validation, and mapping known provider
  failures to HTTP responses.
- **Browser interface (`src/personal_ai_agent/static/index.html`)**: responsive
  chat experience that retains the current conversation in page memory.
- **Configuration (`src/personal_ai_agent/config.py`)**: reads environment
  variables into an immutable settings object. Credentials are not stored in
  source control.
- **Provider client (`src/personal_ai_agent/llm.py`)**: makes one asynchronous
  HTTP request to an OpenAI-compatible chat-completions endpoint and validates
  the response shape.
- **Tests (`tests/`)**: exercise the API and provider boundary with an in-memory
  HTTP transport; tests do not require a live provider or API key.

## Configuration

`OPENAI_API_KEY` is required for `/chat`. `OPENAI_BASE_URL` defaults to
`https://api.openai.com/v1`, `OPENAI_MODEL` defaults to `gpt-4o-mini`, and
`REQUEST_TIMEOUT_SECONDS` defaults to `30`. See `.env.example` and the README.
The application reads process environment variables; it does not automatically
load `.env` files.

## Current limitations

- No task planning, tool registry, persistent memory, task queue, or approval
  workflow.
- Conversation context lasts only while the browser page remains open.
- The provider must implement the OpenAI chat-completions request and response
  format.
- Tests cover mocked provider behavior. A live provider call has not been
  verified without user-supplied credentials.

## Planned evolution

Add capabilities incrementally behind explicit interfaces: first durable,
observable conversation/task state; then a permissioned tool registry and
evidence-based verification. Require human approval for consequential external
actions. Do not execute arbitrary model-generated commands.
