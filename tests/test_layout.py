"""The repo layout is part of the contract: tickets and docs point at these folders."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = ["infra", "services", "schemas", "faults", "mcp", "agents", "bench", "docs"]


@pytest.mark.parametrize("folder", FOLDERS)
def test_folder_exists(folder: str) -> None:
    assert (ROOT / folder).is_dir()


def test_no_env_file_is_tracked() -> None:
    assert not (ROOT / ".env").exists()
