import pytest
from pydantic import ValidationError

from reviewlens_mcp.models import ChangedFile, RepositoryRef


def test_repository_ref_rejects_injection_characters() -> None:
    with pytest.raises(ValidationError):
        RepositoryRef(owner="example/../../etc", repo="demo")


def test_changed_file_rejects_traversal() -> None:
    with pytest.raises(ValidationError):
        ChangedFile(path="../secret", status="added", additions=1, deletions=0)
