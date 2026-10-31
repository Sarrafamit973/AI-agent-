# Personal AI Agent

A small, locally runnable FastAPI service that forwards a user message to a
configurable OpenAI-compatible chat-completions API. This is the project's
working foundation; planning, tools, memory, background jobs, and approvals are
not implemented yet.

## Requirements

- Python 3.10 or later
- An API key for an OpenAI-compatible chat-completions provider to use `/chat`

## Install

Create and activate a virtual environment, then install the project and its
runtime dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For development, including tests:

```powershell
python -m pip install -e ".[dev]"
```

## Configure

Copy `.env.example` to `.env`, set `OPENAI_API_KEY`, and adjust the model or
base URL if needed. The application reads environment variables directly and
does not load `.env` files. For the current PowerShell session, for example:

```powershell
$env:OPENAI_API_KEY = "your-key"
$env:OPENAI_MODEL = "gpt-4o-mini"
```

Available settings:

| Variable | Default | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | unset | Provider credential; required for `/chat` |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | OpenAI-compatible API base URL |
| `OPENAI_MODEL` | `gpt-4o-mini` | Chat-completions model |
| `REQUEST_TIMEOUT_SECONDS` | `30` | Positive per-request timeout |

Do not commit real credentials or `.env` files.

## Run

From the repository root:

```powershell
python -m uvicorn personal_ai_agent.app:app --app-dir src --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API
documentation is at `http://127.0.0.1:8000/docs`.

Check service health:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Send a chat request:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/chat `
  -ContentType "application/json" `
  -Body '{"message":"Hello"}'
```

`/chat` returns `{"reply":"..."}`. It returns HTTP 503 if no API key is
configured, HTTP 422 for invalid input, HTTP 504 on provider timeouts, and HTTP
502 for provider/network errors or an invalid provider response.

## Project layout

```text
app.py                          Root ASGI import for installed deployments
src/personal_ai_agent/
  app.py                        FastAPI application and routes
  config.py                     Environment-backed settings
  llm.py                        OpenAI-compatible provider client
tests/
  test_app.py                   API and provider-boundary tests
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for request flow and boundaries, and
[TESTING.md](./TESTING.md) for verification commands and coverage.

## Current status

Implemented: health endpoint, validated single-message chat endpoint,
configurable asynchronous provider client, explicit upstream error handling,
and mocked automated tests.

Not implemented: task planning, multi-step execution, tools, persistent memory,
background tasks, approval workflows, or a frontend. A live provider request
has not been verified.
