# Architecture

The domain uses Pydantic contracts and ReviewService. GitHubProvider is implemented by deterministic mock and optional live REST providers. MCP and FastAPI are thin adapters over the same service.

This keeps protocol changes independent from review rules, prevents the demo from becoming a second implementation, and supports contract tests without an LLM.

