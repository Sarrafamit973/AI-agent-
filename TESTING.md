# Testing Guide

## 1. General Conversation
Test:
- Simple questions.
- Complex questions.
- Follow-up questions.
- Incorrect or incomplete instructions.

Expected:
- Relevant answers.
- No fabricated tool results.

## 2. Tool Execution
Test:
- Valid tool calls.
- Invalid arguments.
- Tool failures.
- Permission restrictions.

Expected:
- Correct execution.
- Proper error handling.
- No unauthorized actions.

## 3. Planning
Test:
- Multi-step tasks.
- Missing information.
- Conflicting requirements.

Expected:
- Logical task breakdown.
- Correct execution order.

## 4. Verification
Test:
- Incorrect tool output.
- Missing data.
- Failed operations.
- Incorrect calculations.

Expected:
- Errors detected.
- Corrections attempted.
- Unresolved issues reported.

## 5. Memory
Test:
- Store information.
- Retrieve information.
- Update information.
- Delete information.

Expected:
- Correct retrieval.
- No unintended memory changes.

## 6. Security
Test:
- Unauthorized file access.
- Dangerous commands.
- Prompt injection attempts.
- Attempts to bypass approval.

Expected:
- Restricted operations blocked.
- Sensitive information protected.