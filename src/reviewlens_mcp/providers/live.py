import asyncio

import httpx

from ..errors import ProviderError, RateLimitError
from ..models import ChangedFile, PullRequestDetail, PullRequestSummary, RepositoryRef, SearchMatch


class LiveGitHubProvider:
    def __init__(self, token: str | None, timeout_seconds: float = 10.0) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ReviewLens-MCP/0.1",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.AsyncClient(
            base_url="https://api.github.com", headers=headers, timeout=timeout_seconds
        )

    async def _get(
        self,
        path: str,
        *,
        params: dict[str, str | int] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        for attempt in range(2):
            try:
                response = await self._client.get(path, params=params, headers=headers)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                if attempt == 0:
                    await asyncio.sleep(0.2)
                    continue
                raise ProviderError("GitHub request failed after retry", retryable=True) from exc
            if response.status_code in {403, 429} and (
                response.headers.get("x-ratelimit-remaining") == "0" or response.status_code == 429
            ):
                retry_after = response.headers.get("retry-after")
                raise RateLimitError(
                    "GitHub rate limit exceeded", int(retry_after) if retry_after else None
                )
            if response.status_code >= 500 and attempt == 0:
                await asyncio.sleep(0.2)
                continue
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise ProviderError(f"GitHub returned HTTP {response.status_code}") from exc
            return response
        raise ProviderError("GitHub request failed", retryable=True)

    async def list_pull_requests(
        self, repository: RepositoryRef, limit: int
    ) -> list[PullRequestSummary]:
        response = await self._get(
            f"/repos/{repository.owner}/{repository.repo}/pulls",
            params={"state": "open", "per_page": limit},
        )
        return [
            PullRequestSummary(
                number=item["number"],
                title=item["title"],
                author=item["user"]["login"],
                draft=item.get("draft", False),
                updated_at=item["updated_at"],
                url=item["html_url"],
            )
            for item in response.json()
        ]

    async def get_pull_request(self, repository: RepositoryRef, number: int) -> PullRequestDetail:
        item = (
            await self._get(f"/repos/{repository.owner}/{repository.repo}/pulls/{number}")
        ).json()
        return PullRequestDetail(
            number=item["number"],
            title=item["title"],
            author=item["user"]["login"],
            draft=item.get("draft", False),
            updated_at=item["updated_at"],
            url=item["html_url"],
            body=item.get("body") or "",
            base_branch=item["base"]["ref"],
            head_branch=item["head"]["ref"],
            additions=item["additions"],
            deletions=item["deletions"],
            changed_files=item["changed_files"],
        )

    async def get_changed_files(self, repository: RepositoryRef, number: int) -> list[ChangedFile]:
        data = (
            await self._get(
                f"/repos/{repository.owner}/{repository.repo}/pulls/{number}/files",
                params={"per_page": 100},
            )
        ).json()
        return [
            ChangedFile(
                path=item["filename"],
                status=item["status"],
                additions=item["additions"],
                deletions=item["deletions"],
                patch=item.get("patch"),
            )
            for item in data
        ]

    async def get_diff(self, repository: RepositoryRef, number: int) -> str:
        response = await self._get(
            f"/repos/{repository.owner}/{repository.repo}/pulls/{number}",
            headers={"Accept": "application/vnd.github.diff"},
        )
        return response.text

    async def search_code(
        self, repository: RepositoryRef, query: str, limit: int
    ) -> list[SearchMatch]:
        response = await self._get(
            "/search/code",
            params={"q": f"{query} repo:{repository.owner}/{repository.repo}", "per_page": limit},
        )
        return [
            SearchMatch(path=item["path"], line=1, excerpt=f"Search result: {item['name']}")
            for item in response.json().get("items", [])
        ]
