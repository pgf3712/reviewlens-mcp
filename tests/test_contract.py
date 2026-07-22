from reviewlens_mcp.server import mcp


async def test_mcp_exposes_only_expected_read_only_tools() -> None:
    tools = await mcp.list_tools()
    names = {tool.name for tool in tools}
    assert names == {
        "list_pull_requests",
        "get_pull_request",
        "get_pull_request_files",
        "get_pull_request_diff",
        "search_repository_code",
        "find_related_tests",
        "build_review_report",
    }
    mutation_verbs = ("merge", "approve", "comment", "update", "delete", "create")
    assert not any(word in name for name in names for word in mutation_verbs)
