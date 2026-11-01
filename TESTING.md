# Testing Guide

## Install test dependencies

From the repository root, create and activate a virtual environment, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Run automated tests

```powershell
python -m pytest
```

The suite uses FastAPI's test client and an in-memory HTTP transport. It does
not make network requests or require a provider API key.

Current automated coverage includes:

- Browser interface route.
- Health endpoint response.
- Successful chat response, bearer authentication, and conversation context.
- Missing API key and invalid chat input.
- Invalid conversation history.
- Provider timeout and non-success responses.
- Malformed provider response payloads.

## Manual provider smoke test

Set `OPENAI_API_KEY` in the environment, start the application using the
README instructions, then send a `POST /chat` request with a short message.
This makes a real provider request and may incur provider charges. It is
intentionally not part of automated tests.

## Planned coverage

Automated tests for tool permissions, task planning, output verification,
memory controls, background execution, and approval bypass are pending because
those features do not exist yet. Add tests alongside each feature before
marking its task complete.
