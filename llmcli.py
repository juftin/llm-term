"""
LLM CLI
"""

from datetime import datetime, timezone
from textwrap import dedent
from typing import Optional, TypedDict

import click
import openai
import rich.traceback
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

rich.traceback.install(show_locals=True)

__application__ = "llm-cli"
__version__ = "0.2.0"


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


def chat_session(console: Console, system_message: Message, model: str) -> None:
    """
    Chat session with ChatGPT
    """
    messages = [system_message]
    while True:
        text = Prompt.ask("🧑", console=console)
        console.print("")
        if not text:
            continue
        messages.append(Message(role="user", content=text))
        streamed_message = stream_response(
            console=console, messages=messages, model=model
        )
        messages.append(streamed_message)
        console.print("")


def stream_response(console: Console, messages: list[Message], model: str) -> Message:
    """
    Stream the response
    """
    response = openai.ChatCompletion.create(model=model, messages=messages, stream=True)
    complete_message = ""
    with Live(
        Panel(Markdown(complete_message), title="🤖", title_align="left"),
        refresh_per_second=15,
        console=console,
    ) as live:
        for chunk in response:
            if chunk["choices"][0]["finish_reason"] is not None:
                break
            chunk_text = chunk["choices"][0]["delta"].get("content", "")
            complete_message += chunk_text
            live.update(
                Panel(Markdown(complete_message), title="🤖", title_align="left")
            )
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
    type=str,
)
@click.option(
    "--system",
    "-s",
    help="The system message to use",
    envvar="OPENAI_SYSTEM_MESSAGE",
    show_envvar=True,
    default=None,
    type=str,
)
@click.option(
    "--api-key",
    "-k",
    help="The OpenAI API key",
    envvar="OPENAI_API_KEY",
    show_envvar=True,
    type=str,
)
def cli(model: str, system: Optional[str], api_key: str) -> None:
    """
    The LLM-CLI is a command line interface for OpenAI's Chat API.
    """
    console = Console()
    try:
        print_header(console=console, model=model)
        check_credentials(api_key=api_key)
        system_message = setup_system_message(model=model, message=system)
        chat_session(console=console, system_message=system_message, model=model)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    cli()
