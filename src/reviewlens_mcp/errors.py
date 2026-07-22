class ReviewLensError(Exception):
    """Base typed application error."""


class ProviderError(ReviewLensError):
    def __init__(self, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.retryable = retryable


class RateLimitError(ProviderError):
    def __init__(self, message: str, retry_after_seconds: int | None = None) -> None:
        super().__init__(message, retryable=True)
        self.retry_after_seconds = retry_after_seconds
