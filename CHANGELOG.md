# Changelog

Important project changes are recorded here.

## [Unreleased]

### Added
- Responsive browser-based chat interface with in-session conversation context.
- Validation and forwarding for up to 20 prior user/assistant messages.
- Tests covering the interface route and conversation history.

## [0.1.0] - 2026-10-31

### Added
- Minimal FastAPI service with `/health` and validated `POST /chat` endpoints.
- Environment-based configuration and an OpenAI-compatible asynchronous chat
  client.
- Explicit handling for missing credentials, provider timeouts, network
  failures, and malformed provider responses.
- Automated tests using a mocked HTTP transport.
- Installation, configuration, architecture, and test documentation.

### Limitations
- No planning, tool execution, persistent memory, background tasks, approval
  workflow, or frontend.
- The provider integration is tested with mocks; no live API call has been
  verified.
