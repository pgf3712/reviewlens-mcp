from reviewlens_mcp.models import RiskLevel
from reviewlens_mcp.providers.mock import MockGitHubProvider
from reviewlens_mcp.service import ReviewService


async def test_integrated_mock_review_is_structured_and_deterministic() -> None:
    report = await ReviewService(MockGitHubProvider()).build_review_report(
        "example", "checkout-service", 42
    )
    assert report.repository == "example/checkout-service"
    assert report.risk_level is RiskLevel.MEDIUM
    assert report.related_tests == ["tests/test_webhook_verification.py"]
    assert report.injection_signals[0].location == "pull_request.body"
    assert len(report.evidence) == 3


async def test_diff_is_bounded() -> None:
    result = await ReviewService(MockGitHubProvider(), max_diff_chars=40).get_diff(
        "example", "checkout-service", 42
    )
    assert result["truncated"] is True
    assert len(result["diff"]) == 40
