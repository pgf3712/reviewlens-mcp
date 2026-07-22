from .config import Settings
from .providers import LiveGitHubProvider, MockGitHubProvider
from .service import ReviewService


def create_service(settings: Settings | None = None) -> ReviewService:
    settings = settings or Settings()
    provider = (
        MockGitHubProvider()
        if settings.mode == "mock"
        else LiveGitHubProvider(settings.github_token, settings.http_timeout_seconds)
    )
    return ReviewService(provider, settings.max_diff_chars)
