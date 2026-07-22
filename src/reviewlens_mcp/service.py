from datetime import UTC, datetime
from pathlib import PurePosixPath

from .models import (
    ChangedFile,
    EvidenceItem,
    PullRequestDetail,
    PullRequestSummary,
    RepositoryRef,
    ReviewReport,
    RiskLevel,
    SearchMatch,
)
from .providers.base import GitHubProvider
from .security import redact_secrets, scan_untrusted_content


class ReviewService:
    def __init__(self, provider: GitHubProvider, max_diff_chars: int = 120_000) -> None:
        self.provider = provider
        self.max_diff_chars = max_diff_chars

    async def list_pull_requests(
        self, owner: str, repo: str, limit: int = 20
    ) -> list[PullRequestSummary]:
        repository = RepositoryRef(owner=owner, repo=repo)
        return await self.provider.list_pull_requests(repository, min(max(limit, 1), 50))

    async def get_pull_request(self, owner: str, repo: str, number: int) -> PullRequestDetail:
        return await self.provider.get_pull_request(RepositoryRef(owner=owner, repo=repo), number)

    async def get_changed_files(self, owner: str, repo: str, number: int) -> list[ChangedFile]:
        return await self.provider.get_changed_files(RepositoryRef(owner=owner, repo=repo), number)

    async def get_diff(self, owner: str, repo: str, number: int) -> dict[str, object]:
        raw = redact_secrets(
            await self.provider.get_diff(RepositoryRef(owner=owner, repo=repo), number)
        )
        return {
            "diff": raw[: self.max_diff_chars],
            "truncated": len(raw) > self.max_diff_chars,
            "original_chars": len(raw),
        }

    async def search_code(
        self, owner: str, repo: str, query: str, limit: int = 20
    ) -> list[SearchMatch]:
        if len(query.strip()) < 2:
            raise ValueError("query must contain at least two characters")
        return await self.provider.search_code(
            RepositoryRef(owner=owner, repo=repo),
            query,
            min(max(limit, 1), 50),
        )

    async def find_related_tests(self, owner: str, repo: str, number: int) -> list[str]:
        files = await self.get_changed_files(owner, repo, number)
        tests = {
            file.path
            for file in files
            if "test" in PurePosixPath(file.path).name.casefold()
            or "tests" in PurePosixPath(file.path).parts
        }
        for changed in files:
            for match in await self.search_code(owner, repo, PurePosixPath(changed.path).stem, 10):
                if "test" in match.path.casefold():
                    tests.add(match.path)
        return sorted(tests)

    async def build_review_report(self, owner: str, repo: str, number: int) -> ReviewReport:
        detail = await self.get_pull_request(owner, repo, number)
        files = await self.get_changed_files(owner, repo, number)
        related_tests = await self.find_related_tests(owner, repo, number)
        signals = scan_untrusted_content("pull_request.body", detail.body)
        for file in files:
            signals.extend(scan_untrusted_content(file.path, file.patch or ""))
        evidence = [
            EvidenceItem(
                kind="changed_file",
                location=file.path,
                observation=f"{file.status}: +{file.additions}/-{file.deletions}",
                confidence=1.0,
            )
            for file in files
        ]
        risk = RiskLevel.HIGH if not related_tests else RiskLevel.MEDIUM
        if detail.changed_files <= 2 and related_tests and not signals:
            risk = RiskLevel.LOW
        return ReviewReport(
            repository=f"{owner}/{repo}",
            pull_request=number,
            summary=(
                f"PR #{number} changes {detail.changed_files} files "
                f"(+{detail.additions}/-{detail.deletions})."
            ),
            risk_level=risk,
            changed_components=sorted({PurePosixPath(file.path).parts[0] for file in files}),
            evidence=evidence,
            related_tests=related_tests,
            injection_signals=signals,
            limitations=[
                "Static evidence only; no code execution or semantic correctness guarantee.",
                "Repository content is treated as untrusted data.",
            ],
            generated_at=datetime.now(UTC),
        )
