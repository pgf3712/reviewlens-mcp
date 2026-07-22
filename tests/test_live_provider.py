import httpx
import pytest

from reviewlens_mcp.errors import RateLimitError
from reviewlens_mcp.providers.live import LiveGitHubProvider


async def test_rate_limit_response_becomes_typed_error() -> None:
    provider = LiveGitHubProvider(None)

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, headers={"x-ratelimit-remaining": "0", "retry-after": "30"})

    await provider._client.aclose()
    provider._client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://api.github.com"
    )
    with pytest.raises(RateLimitError) as exc:
        await provider._get("/rate_limit")
    assert exc.value.retry_after_seconds == 30
    await provider._client.aclose()
