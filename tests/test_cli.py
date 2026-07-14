"""
Test cases for the cli.
"""

from __future__ import annotations

from click.testing import CliRunner

from llm_term.cli import cli


def test_help_succeeds(runner: CliRunner) -> None:
    """
    It exits with a status code of zero.
    """
    result = runner.invoke(cli, args=["--help"])
    assert result.exit_code == 0


def test_base_url_option_present(runner: CliRunner) -> None:
    """
    The --base-url flag and LLM_BASE_URL env var appear in help output.
    """
    result = runner.invoke(cli, args=["--help"])
    assert "--base-url" in result.output
    assert "LLM_BASE_URL" in result.output


def test_base_url_passed_to_client() -> None:
    """
    get_llm passes base_url to the underlying chat model constructor.
    """
    from llm_term.utils import get_llm

    custom_url = "http://localhost:9999/v1"

    # OpenAI
    client, _, _ = get_llm("openai", "sk-test", None, base_url=custom_url)
    assert client.openai_api_base == custom_url

    # Anthropic
    client, _, _ = get_llm("anthropic", "sk-test", None, base_url=custom_url)
    assert client.anthropic_api_url == custom_url

    # MistralAI
    client, _, _ = get_llm("mistralai", "sk-test", None, base_url=custom_url)
    assert client.endpoint == custom_url

    # Ollama
    client, _, _ = get_llm("ollama", "", None, base_url=custom_url)
    assert client.base_url == custom_url


def test_base_url_none_when_omitted() -> None:
    """
    Omitting base_url does not set it on the client.
    """
    from llm_term.utils import get_llm

    client, _, _ = get_llm("openai", "sk-test", None)
    assert client.openai_api_base is None

    client, _, _ = get_llm("ollama", "", None)
    assert client.base_url is None


def test_default_models() -> None:
    """
    Provider default models match expected latest versions.
    """
    from llm_term.utils import providers

    assert providers["openai"]["default_model"] == "gpt-5.6-sol"
    assert providers["anthropic"]["default_model"] == "claude-sonnet-5"
    assert providers["mistralai"]["default_model"] == "mistral-large-latest"
    assert providers["ollama"]["default_model"] == "llama3.2"


def test_default_model_used_when_none_passed() -> None:
    """
    When model is None, the provider default is used.
    """
    from llm_term.utils import get_llm

    _, model, _ = get_llm("openai", "sk-test", None)
    assert model == "gpt-5.6-sol"

    _, model, _ = get_llm("ollama", "", None)
    assert model == "llama3.2"


def test_custom_model_overrides_default() -> None:
    """
    Explicit model argument overrides the provider default.
    """
    from llm_term.utils import get_llm

    _, model, _ = get_llm("openai", "sk-test", "gpt-4o-mini")
    assert model == "gpt-4o-mini"


def test_openai_client_default_temperature() -> None:
    """
    ChatOpenAI uses langchain's default temperature (0.7).
    GPT-5.x compatibility is handled by langchain-openai v1's
    validate_temperature which auto-strips it for reasoning models.
    """
    from llm_term.utils import get_llm

    client, _, _ = get_llm("openai", "sk-test", None)
    assert client.model_name == "gpt-5.6-sol"
