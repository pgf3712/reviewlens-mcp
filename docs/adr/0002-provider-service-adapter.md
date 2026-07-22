# ADR 0002: Provider, service, adapter separation

Status: Accepted

Decision: Keep typed domain orchestration independent from providers and transports. Putting logic in MCP tools was rejected because it duplicates logic and weakens testing.

Consequence: More files, but deterministic tests and replaceable adapters.

