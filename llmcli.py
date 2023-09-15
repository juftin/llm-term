"""
LLM CLI
"""

from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, Generator, Optional, TypedDict

import click
import openai
import rich.traceback
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner

rich.traceback.install(show_locals=True)

__application__ = "llm-cli"
__version__ = "0.3.0"


class Message(TypedDict):
    """
    Message
    """

    role: str
    content: str


def print_header(console: Console, model: str) -> None:
    """
    Print the header
    """
    console.print(
        Panel(
            f"[bold red]{__application__} is a command line interface for OpenAI's Chat API[/bold red]",
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
        raise click.ClickException(
            "You must set the OPENAI_API_KEY environment variable or set the `--api-key` / `-k` option"
        )


def setup_system_message(model: str, message: Optional[str] = None) -> Message:
    """
    Set up the system message
    """
    now_utc = datetime.now(timezone.utc)
    setup = f"""
        You are a helpful AI assistant named {__application__}, built by OpenAI and based on 
        the model {model}. Help the user by responding to their request, the output should 
        be concise and always written in markdown. Ensure that all code blocks have the correct 
        language tag.

        The current date and time at the start of this conversation is  
        {datetime.now()} {now_utc.astimezone().tzinfo.tzname(now_utc)}.
        """
    system_message = message or dedent(setup).strip()
    return Message(role="system", content=system_message)


def chat_session(
    console: Console, system_message: Message, model: str, stream: bool
) -> None:
    """
    Chat session with ChatGPT
    """
    history = Path().home() / ".llm-cli-history.txt"
    session = PromptSession(history=FileHistory(str(history)))
    messages = [system_message]
    while True:
        text = session.prompt("🧑: ", auto_suggest=AutoSuggestFromHistory())
        console.print("")
        if not text:
            continue
        messages.append(Message(role="user", content=text))
        streamed_message = print_response(
            console=console,
            messages=messages,
            model=model,
            stream=stream,
        )
        messages.append(streamed_message)
        console.print("")


def print_response(
    console: Console, messages: list[Message], model: str, stream: bool
) -> Message:
    """
    Stream the response
    """
    if stream is False:
        with Live(
            Spinner("aesthetic"), refresh_per_second=15, console=console, transient=True
        ):
            response = openai.ChatCompletion.create(
                model=model, messages=messages, stream=False
            )
            complete_response = response["choices"][0]["message"]["content"]
            console.print(
                Panel(Markdown(complete_response), title="🤖", title_align="left")
            )
        message = Message(role="assistant", content=complete_response)
    else:
        response = openai.ChatCompletion.create(
            model=model, messages=messages, stream=True
        )
        message = render_streamed_response(response=response, console=console)
    return message


def render_streamed_response(
    response: Generator[Dict[str, Any], None, None], console: Console
) -> Message:
    """
    Render the streamed response and a spinner
    """
    complete_message = ""
    rich_response = Columns(
        [
            Panel(Markdown(complete_message), title="🤖", title_align="left"),
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
                    Panel(Markdown(complete_message), title="🤖", title_align="left"),
                    Spinner("aesthetic"),
                ]
            )
            live.update(updated_response)
        live.update(Panel(Markdown(complete_message), title="🤖", title_align="left"))
    return Message(role="assistant", content=complete_message)


@click.command()
@click.version_option(version=__version__, prog_name=__application__)
@click.option(
    "--model",
    "-m",
    help="The GPT model to use",
    envvar="OPENAI_MODEL",
    show_envvar=True,
    default="gpt-3.5-turbo",
    type=click.STRING,
)
@click.option(
    "--system",
    "-s",
    help="The system message to use",
    envvar="OPENAI_SYSTEM_MESSAGE",
    show_envvar=True,
    default=None,
    type=click.STRING,
)
@click.option(
    "--api-key",
    "-k",
    help="The OpenAI API key",
    envvar="OPENAI_API_KEY",
    show_envvar=True,
    type=click.STRING,
)
@click.option(
    "--stream/--no-stream",
    help="Stream the response",
    envvar="OPENAI_STREAM",
    show_envvar=True,
    default=True,
    type=click.BOOL,
)
@click.option(
    "--console",
    "-c",
    help="The console width to use - defaults to auto-detect",
    type=click.INT,
    default=None,
)
def cli(
    model: str, system: Optional[str], api_key: str, stream: bool, console: int
) -> None:
    """
    The LLM-CLI is a command line interface for OpenAI's Chat API.
    """
    console = Console(width=console)
    try:
        print_header(console=console, model=model)
        check_credentials(api_key=api_key)
        system_message = setup_system_message(model=model, message=system)
        chat_session(
            console=console, system_message=system_message, model=model, stream=stream
        )
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    cli()
