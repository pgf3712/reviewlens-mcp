from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RepositoryRef(BaseModel):
    owner: str = Field(pattern=r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
    repo: str = Field(pattern=r"^[A-Za-z0-9._-]{1,100}$")


class PullRequestSummary(BaseModel):
    number: int = Field(gt=0)
    title: str = Field(max_length=500)
    author: str
    draft: bool = False
    updated_at: datetime
    url: str


class PullRequestDetail(PullRequestSummary):
    body: str = Field(default="", max_length=50_000)
    base_branch: str
    head_branch: str
    additions: int = Field(ge=0)
    deletions: int = Field(ge=0)
    changed_files: int = Field(ge=0)


class ChangedFile(BaseModel):
    path: str
    status: str
    additions: int = Field(ge=0)
    deletions: int = Field(ge=0)
    patch: str | None = None

    @field_validator("path")
    @classmethod
    def relative_safe_path(cls, value: str) -> str:
        normalized = value.replace("\\", "/")
        if normalized.startswith("/") or ".." in normalized.split("/"):
            raise ValueError("path must be repository-relative and cannot traverse directories")
        return normalized


class SearchMatch(BaseModel):
    path: str
    line: int = Field(gt=0)
    excerpt: str = Field(max_length=1_000)


class InjectionSignal(BaseModel):
    location: str
    pattern: str
    explanation: str


class EvidenceItem(BaseModel):
    kind: str
    location: str
    observation: str
    confidence: float = Field(ge=0, le=1)


class ReviewReport(BaseModel):
    repository: str
    pull_request: int
    summary: str
    risk_level: RiskLevel
    changed_components: list[str]
    evidence: list[EvidenceItem]
    related_tests: list[str]
    injection_signals: list[InjectionSignal]
    limitations: list[str]
    generated_at: datetime
