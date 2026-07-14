"""
Helper functions for the CLI
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from textwrap import dedent
from typing import TypedDict

from click.exceptions import ClickException
from langchain_core.language_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    BaseMessageChunk,
    HumanMessage,
    SystemMessage,
)
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner

from llm_term.__about__ import __application__, __version__
from llm_term.base import NoPadding


def print_header(console: Console, model: str, provider: str) -> None:
    """
    Print the header
    """
    renderable = (
        "[bold cyan]  ✺✺✺✺   [/bold cyan]"
        f"[bold red]{provider}[/bold red]"
        "[bold cyan]   ✺✺✺✺  [/bold cyan]"
    )
    console.print(
        Panel(
            Align(renderable=renderable, align="center"),
            title=f"[blue bold]{__application__} v{__version__}[/blue bold]",
            subtitle=f"[yellow bold]{model}[/yellow bold]",
            style="green bold",
            expand=False,
        ),
    )
    console.print("")


class ProviderConfig(TypedDict):
    """
    Model configuration
    """

    default_model: str
    name: str


providers: dict[str, ProviderConfig] = {
    "openai": ProviderConfig(default_model="gpt-5.6-sol", name="OpenAI"),
    "anthropic": ProviderConfig(default_model="claude-sonnet-5", name="Anthropic"),
    "mistralai": ProviderConfig(default_model="mistral-large-latest", name="MistralAI"),
    "ollama": ProviderConfig(default_model="llama3.2", name="Ollama"),
}


def get_llm(
    provider: str, api_key: str, model: str | None, base_url: str | None = None
) -> tuple[BaseChatModel | BaseLLM, str, str]:
    """
    Check the credentials and return the appropriate LLM client.

    Parameters
    ----------
    provider : str
        The LLM provider to use (openai, anthropic, mistralai, ollama).
    api_key : str
        The API key for the provider.
    model : str | None
        The model name to use, or None to use the provider default.
    base_url : str | None
        An optional base URL for the API endpoint.

    Returns
    -------
    tuple[BaseChatModel | BaseLLM, str, str]
        The LLM client, the model name, and the provider display name.
    """
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        chat_model = model or providers[provider]["default_model"]
        provider_name = providers[provider]["name"]
        kwargs: dict[str, str] = {"openai_api_key": api_key, "model_name": chat_model}
        if base_url:
            kwargs["openai_api_base"] = base_url
        return ChatOpenAI(**kwargs), chat_model, provider_name
    elif provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic

            chat_model = model or providers[provider]["default_model"]
            provider_name = providers[provider]["name"]
            kwargs = {"anthropic_api_key": api_key, "model": chat_model}
            if base_url:
                kwargs["anthropic_api_url"] = base_url
            return (
                ChatAnthropic(**kwargs),
                chat_model,
                provider_name,
            )
        except ImportError as ie:
            msg = (
                "The `anthropic` provider requires the `anthropic` extra to be installed: "
                'pipx install "llm-term[anthropic]"'
            )
            raise ClickException(msg) from ie
    elif provider == "mistralai":
        try:
            from langchain_mistralai import ChatMistralAI

            chat_model = model or providers[provider]["default_model"]
            provider_name = providers[provider]["name"]
            kwargs = {"mistral_api_key": api_key, "model": chat_model}
            if base_url:
                kwargs["endpoint"] = base_url
            return (
                ChatMistralAI(**kwargs),
                chat_model,
                provider_name,
            )
        except ImportError as ie:
            msg = (
                "The `mistralai` provider requires the `mistralai` extra to be installed: "
                'pipx install "llm-term[mistralai]"'
            )
            raise ClickException(msg) from ie
    elif provider == "ollama":
        from langchain_ollama import ChatOllama

        chat_model = model or providers[provider]["default_model"]
        provider_name = providers[provider]["name"]
        kwargs = {"model": chat_model}
        if base_url:
            kwargs["base_url"] = base_url
        return ChatOllama(**kwargs), chat_model, provider_name
    else:
        msg = f"Provider {provider} is not supported... yet"
        raise ClickException(msg)


def setup_system_message(message: str | None = None) -> SystemMessage:
    """
    Set up the system message
    """
    setup = f"""
        You are a helpful AI assistant named {__application__}. Help the user by responding to
        their request, the output should be concise and always written in markdown format.
        Answer questions only if you know the answer or can make a well-informed guess;
        otherwise tell the you don't know or ask for more information.
        """
    system_message = message or dedent(setup).strip()
    return SystemMessage(content=system_message)


def chat_session(
    client: BaseChatModel | BaseLLM,
    console: Console,
    system_message: SystemMessage,
    stream: bool,
    panel: bool,
    chat_message: str,
    avatar: str,
) -> None:
    """
    Chat session with ChatGPT
    """
    history_file = Path().home() / ".llm-term-history.txt"
    history = FileHistory(str(history_file))
    session: PromptSession = PromptSession(history=history, erase_when_done=True)
    messages: list[BaseMessage] = [system_message]
    if chat_message.strip() != "":
        messages.append(HumanMessage(content=chat_message))
    message_counter = 0
    while True:
        if message_counter == 0 and len(messages) == 2:  # noqa: PLR2004
            console.print(f"{avatar}: {chat_message}")
            history.append_string(chat_message)
            if panel is False:
                console.print("")
                console.rule()
        else:
            text = session.prompt(f"{avatar}: ", auto_suggest=AutoSuggestFromHistory())
            if not text:
                continue
            console.print(f"{avatar}: {text}")
            if panel is False:
                console.print("")
                console.rule()
            messages.append(HumanMessage(content=text))
        console.print("")
        streamed_message = print_response(
            client=client,
            console=console,
            messages=messages,
            stream=stream,
            panel=panel,
        )
        if panel is False:
            console.print("")
            console.rule()
        messages.append(streamed_message)
        console.print("")
        message_counter += 1


def print_response(
    client: BaseChatModel | BaseLLM,
    console: Console,
    messages: list[BaseMessage],
    stream: bool,
    panel: bool,
) -> AIMessage:
    """
    Stream the response
    """
    panel_class = Panel if panel is True else NoPadding
    if stream is False:
        with Live(Spinner("aesthetic"), refresh_per_second=15, console=console, transient=True):
            response = client.invoke(input=messages)
            if isinstance(response, BaseMessage):
                text = response.content or ""
            else:
                text = response or ""
            console.print(panel_class(Markdown(response.content), title="🤖", title_align="left"))
        message = AIMessage(content=text)
    else:
        response = client.stream(input=messages)
        message = render_streamed_response(response=response, console=console, panel=panel)
    return message


def render_streamed_response(
    response: Iterator[BaseMessageChunk | str], console: Console, panel: bool
) -> AIMessage:
    """
    Render the streamed response and a spinner
    """
    panel_class = Panel if panel is True else NoPadding
    complete_message = ""
    rich_response = Columns(
        [
            panel_class(Markdown(complete_message), title="🤖", title_align="left"),
            Spinner("aesthetic"),
        ]
    )
    with Live(
        rich_response,
        refresh_per_second=15,
        console=console,
    ) as live:
        for chunk in response:
            if isinstance(chunk, BaseMessageChunk):
                chunk_text = chunk.content or ""
            else:
                chunk_text = chunk or ""
            complete_message += chunk_text
            updated_response = Columns(
                [
                    panel_class(Markdown(complete_message), title="🤖", title_align="left"),
                    Spinner("aesthetic"),
                ]
            )
            live.update(updated_response)
        live.update(panel_class(Markdown(complete_message), title="🤖", title_align="left"))
    return AIMessage(content=complete_message)
