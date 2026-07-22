import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from .factory import create_service
from .logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
mcp = FastMCP("ReviewLens MCP", json_response=True)
service = create_service()


@mcp.tool()
async def list_pull_requests(owner: str, repo: str, limit: int = 20) -> list[dict[str, Any]]:
    """List open pull requests without changing the repository."""
    return [
        item.model_dump(mode="json")
        for item in await service.list_pull_requests(owner, repo, limit)
    ]


@mcp.tool()
async def get_pull_request(owner: str, repo: str, number: int) -> dict[str, Any]:
    """Get typed pull-request metadata."""
    return (await service.get_pull_request(owner, repo, number)).model_dump(mode="json")


@mcp.tool()
async def get_pull_request_files(owner: str, repo: str, number: int) -> list[dict[str, Any]]:
    """Get changed files and patches for a pull request."""
    return [
        item.model_dump(mode="json")
        for item in await service.get_changed_files(owner, repo, number)
    ]


@mcp.tool()
async def get_pull_request_diff(owner: str, repo: str, number: int) -> dict[str, object]:
    """Get a bounded, redacted unified diff."""
    return await service.get_diff(owner, repo, number)


@mcp.tool()
async def search_repository_code(
    owner: str, repo: str, query: str, limit: int = 20
) -> list[dict[str, Any]]:
    """Search code in a repository using a bounded query."""
    return [
        item.model_dump(mode="json")
        for item in await service.search_code(owner, repo, query, limit)
    ]


@mcp.tool()
async def find_related_tests(owner: str, repo: str, number: int) -> list[str]:
    """Find test paths related to changed files."""
    return await service.find_related_tests(owner, repo, number)


@mcp.tool()
async def build_review_report(owner: str, repo: str, number: int) -> dict[str, Any]:
    """Build deterministic structured evidence; never asks an LLM for a verdict."""
    logger.info(
        "Building evidence report for %s/%s#%s",
        owner,
        repo,
        number,
        extra={"event": "review_report_requested"},
    )
    return (await service.build_review_report(owner, repo, number)).model_dump(mode="json")


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
