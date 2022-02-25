"""Fixtures and helpers for the PUDL Zenodo Storage tests."""
from random import randint
from uuid import uuid4

import pytest


@pytest.fixture()
def zenodo_url() -> str:
    """Create a fake Zenodo deposit URL."""
    depid = randint(10000, 99999)
    uuid = uuid4()
    return f"https://zenodo.org/api/deposit/depositions/{depid}/files/{uuid}"
