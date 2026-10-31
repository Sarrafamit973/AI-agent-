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
    |-- GET /health
    |-- POST /chat
    |       |
    |       +-- request validation (Pydantic)
    |       +-- LLM client (src/personal_ai_agent/llm.py)
    |               |
    |               +-- configured chat-completions HTTP endpoint
    |
    +-- settings loaded from environment (src/personal_ai_agent/config.py)
```

## Request flow

1. `POST /chat` accepts a non-empty `message` of at most 10,000 characters.
2. FastAPI validates the request. Invalid input receives HTTP 422.
3. The application checks that `OPENAI_API_KEY` is configured. If it is not,
   the request receives HTTP 503; health checks remain available.
4. The LLM client sends one user message to
   `{OPENAI_BASE_URL}/chat/completions`, using the configured model and timeout.
5. A valid provider response is returned as `{"reply": "..."}`. Provider
   timeouts return HTTP 504; provider/network errors or malformed responses
   return HTTP 502. Error responses do not include provider bodies or secrets.

## Components and boundaries

- **API (`app.py`, `src/personal_ai_agent/app.py`)**: ASGI entry point, HTTP
  routes, request validation, and mapping known provider failures to HTTP
  responses.
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

- No conversation history, planning, tool registry, memory, task queue, approval
  workflow, or user interface.
- Only a single user message is sent per request; prior turns are not retained.
- The provider must implement the OpenAI chat-completions request and response
  format.
- Tests cover mocked provider behavior. A live provider call has not been
  verified without user-supplied credentials.

## Planned evolution

Add capabilities incrementally behind explicit interfaces: first durable,
observable conversation/task state; then a permissioned tool registry and
evidence-based verification. Require human approval for consequential external
actions. Do not execute arbitrary model-generated commands.
