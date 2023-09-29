"""
Shared fixtures for tests.
"""

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    """
    Fixture for invoking command-line interfaces.
    """
    return CliRunner()
