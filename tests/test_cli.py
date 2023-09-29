"""
Test cases for the cli.
"""

from click.testing import CliRunner

from llm_term.cli import cli


def test_main_succeeds(runner: CliRunner) -> None:
    """
    It exits with a status code of zero.
    """
    result = runner.invoke(cli, args=["--help"])
    assert result.exit_code == 0
