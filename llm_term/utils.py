"""
Helper functions for the CLI
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Any, Generator

import click
import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner

from llm_term.__about__ import __application__, __version__
from llm_term.base import Message, NoPadding


def print_header(console: Console, model: str) -> None:
    """
    Print the header
    """
    console.print(
        Panel(
            f"[bold red]{__application__} "
            f"is a command line interface for OpenAI's Chat API[/bold red]",
            title=f"[blue bold]{__application__} v{__version__}[/blue bold]",
            subtitle=f"[yellow bold]{model}[/yellow bold]",
            style="green bold",
            expand=False,
        ),
    )
    console.print("")


def check_credentials(api_key: str) -> None:
    """
    Check the credentials
    """
    if api_key is not None:
        openai.api_key = api_key
    else:
        msg = (
            "You must set the OPENAI_API_KEY environment variable "
            "or set the `--api-key` / `-k` option"
        )
        raise click.ClickException(msg)


def setup_system_message(model: str, message: str | None = None) -> Message:
    """
    Set up the system message
    """
    setup = f"""
        You are a helpful AI assistant named {__application__}, built by OpenAI and based on
        the model {model}. Help the user by responding to their request, the output should
        be concise and always written in markdown. Ensure that all code blocks have the correct
        language tag.

        The current UTC date and time at the start of this conversation is
        {datetime.now(tz=timezone.utc).isoformat()}
        """
    system_message = message or dedent(setup).strip()
    return Message(role="system", content=system_message)


def chat_session(
    console: Console,
    system_message: Message,
    model: str,
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
    messages: list[Message] = [system_message]
    if chat_message.strip() != "":
        messages.append(Message(role="user", content=chat_message))
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
            messages.append(Message(role="user", content=text))
        console.print("")
        streamed_message = print_response(
            console=console,
            messages=messages,
            model=model,
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
    console: Console, messages: list[Message], model: str, stream: bool, panel: bool
) -> Message:
    """
    Stream the response
    """
    panel_class = Panel if panel is True else NoPadding
    if stream is False:
        with Live(Spinner("aesthetic"), refresh_per_second=15, console=console, transient=True):
            response = openai.ChatCompletion.create(model=model, messages=messages, stream=False)
            complete_response = response["choices"][0]["message"]["content"]
            console.print(panel_class(Markdown(complete_response), title="🤖", title_align="left"))
        message = Message(role="assistant", content=complete_response)
    else:
        response = openai.ChatCompletion.create(model=model, messages=messages, stream=True)
        message = render_streamed_response(response=response, console=console, panel=panel)
    return message


def render_streamed_response(
    response: Generator[dict[str, Any], None, None], console: Console, panel: bool
) -> Message:
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
            if chunk["choices"][0]["finish_reason"] is not None:
                break
            chunk_text = chunk["choices"][0]["delta"].get("content", "")
            complete_message += chunk_text
            updated_response = Columns(
                [
                    panel_class(Markdown(complete_message), title="🤖", title_align="left"),
                    Spinner("aesthetic"),
                ]
            )
            live.update(updated_response)
        live.update(panel_class(Markdown(complete_message), title="🤖", title_align="left"))
    return Message(role="assistant", content=complete_message)
