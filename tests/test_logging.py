import json
import logging

from reviewlens_mcp.logging_config import JsonFormatter


def test_structured_logging_redacts_tokens() -> None:
    synthetic_token = "ghp_" + "abcdefghijklmnopqrstuvwxyz123456"
    record = logging.LogRecord(
        name="reviewlens",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg=f"credential {synthetic_token}",
        args=(),
        exc_info=None,
    )
    payload = json.loads(JsonFormatter().format(record))
    assert payload["level"] == "INFO"
    assert "[REDACTED]" in payload["message"]
    assert "ghp_" not in payload["message"]
