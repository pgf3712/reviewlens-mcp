from typing import Protocol

from ..models import ChangedFile, PullRequestDetail, PullRequestSummary, RepositoryRef, SearchMatch


class GitHubProvider(Protocol):
    async def list_pull_requests(
        self, repository: RepositoryRef, limit: int
    ) -> list[PullRequestSummary]: ...

    async def get_pull_request(
        self, repository: RepositoryRef, number: int
    ) -> PullRequestDetail: ...

    async def get_changed_files(
        self, repository: RepositoryRef, number: int
    ) -> list[ChangedFile]: ...

    async def get_diff(self, repository: RepositoryRef, number: int) -> str: ...

    async def search_code(
        self, repository: RepositoryRef, query: str, limit: int
    ) -> list[SearchMatch]: ...
