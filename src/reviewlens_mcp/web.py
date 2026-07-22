from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .factory import create_service
from .logging_config import configure_logging

configure_logging()
app = FastAPI(title="ReviewLens MCP Demo", docs_url=None, redoc_url=None)
service = create_service()
static_dir = Path(__file__).parent / "static"
app.mount("/assets", StaticFiles(directory=static_dir), name="assets")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/api/demo/review")
async def demo_review() -> dict[str, Any]:
    report = await service.build_review_report("example", "checkout-service", 42)
    return report.model_dump(mode="json")


@app.get("/api/tools")
async def tools() -> list[dict[str, object]]:
    return [
        {
            "name": "list_pull_requests",
            "purpose": "List open PRs",
            "inputs": ["owner", "repo", "limit"],
        },
        {
            "name": "get_pull_request",
            "purpose": "Fetch PR metadata",
            "inputs": ["owner", "repo", "number"],
        },
        {
            "name": "get_pull_request_files",
            "purpose": "Collect changed files",
            "inputs": ["owner", "repo", "number"],
        },
        {
            "name": "get_pull_request_diff",
            "purpose": "Return a bounded redacted diff",
            "inputs": ["owner", "repo", "number"],
        },
        {
            "name": "search_repository_code",
            "purpose": "Search repository code",
            "inputs": ["owner", "repo", "query", "limit"],
        },
        {
            "name": "find_related_tests",
            "purpose": "Locate related tests",
            "inputs": ["owner", "repo", "number"],
        },
        {
            "name": "build_review_report",
            "purpose": "Assemble structured evidence",
            "inputs": ["owner", "repo", "number"],
        },
    ]


def main() -> None:
    import uvicorn

    uvicorn.run("reviewlens_mcp.web:app", host="127.0.0.1", port=8000)
