# Development Tasks

## Phase 1: Foundation

- [x] Configure Python package structure and dependency management.
- [x] Implement configurable OpenAI-compatible chat API and conversation
  endpoint (mocked provider tests; live credentials not verified).
- [x] Add health endpoint and automated API tests.
- [ ] Verify a chat request against a real provider using a locally configured
  API key.

## Phase 2: Tool Execution

- [ ] Define a permission-aware tool interface and registry.
- [ ] Add narrowly scoped file operations.
- [ ] Design safe execution for supported code tasks; do not run unrestricted
  model-generated commands.
- [ ] Add tool failure handling and audit records.

## Phase 3: Agent Workflows

- [ ] Add explicit task planning and execution state.
- [ ] Add bounded retries and progress reporting.

## Phase 4: Verification

- [ ] Verify task outputs against explicit requirements and evidence.
- [ ] Add correction and failure-reporting flows.

## Phase 5: Memory

- [ ] Design inspectable, user-controlled conversation and project memory.

## Phase 6: Background Tasks and Human Approval

- [ ] Add bounded background execution, status, and cancellation.
- [ ] Require approval for consequential external actions.

## Phase 7: Interface

- [x] Add a browser-based conversation interface with temporary chat context.
- [ ] Build task tracking, tool activity, and approval views as their backend
  capabilities are implemented.
