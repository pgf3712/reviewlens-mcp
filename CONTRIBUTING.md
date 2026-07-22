# Contributing

Keep the MCP surface read-only. New tools must have typed inputs and outputs, deterministic tests, documented failure behavior, and a clear reason they cannot be composed from existing tools.

Before opening a pull request, run:

    ruff format --check .
    ruff check .
    mypy src
    pytest

Never commit tokens, private repository fixtures, copied proprietary diffs, or audio without a compatible license entry.

