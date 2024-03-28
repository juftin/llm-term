"""
LLM CLI
"""

from __future__ import annotations

import click
import rich.traceback
from rich.console import Console

from llm_term.__about__ import __application__, __version__
from llm_term.utils import chat_session, get_llm, print_header, providers, setup_system_message

rich.traceback.install(show_locals=True)


@click.command()
@click.version_option(version=__version__, prog_name=__application__)
@click.option(
    "--model",
    "-m",
    help="The LLM model to use",
    envvar="LLM_MODEL",
    show_envvar=True,
    default=None,
    type=click.STRING,
)
@click.option(
    "--provider",
    "-p",
    help="The LLM provider to use",
    envvar="LLM_PROVIDER",
    show_envvar=True,
    default="openai",
    type=click.Choice(providers),
)
@click.argument(
    "chat",
    nargs=-1,
    type=click.STRING,
    default=None,
)
@click.option(
    "--system",
    "-s",
    help="The system message to use",
    envvar="LLM_SYSTEM_MESSAGE",
    show_envvar=True,
    default=None,
    type=click.STRING,
)
@click.option(
    "--api-key",
    "-k",
    help="The API key to use",
    envvar="LLM_API_KEY",
    show_envvar=True,
    type=click.STRING,
)
@click.option(
    "--stream/--no-stream",
    help="Stream the response",
    envvar="LLM_STREAM",
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
@click.option(
    "--border/--no-border",
    help="Use a border for returned responses - disable for copy/paste",
    default=True,
    type=click.BOOL,
)
@click.option(
    "--avatar",
    "-a",
    help="The avatar to use",
    type=click.STRING,
    default="🤓",
    show_default=True,
)
def cli(
    model: str,
    chat: tuple[str, ...],
    system: str | None,
    api_key: str,
    stream: bool,
    console: int,
    border: bool,
    avatar: str,
    provider: str,
) -> None:
    """
    llm-term is a command line interface for OpenAI's Chat API.
    """
    rich_console: Console = Console(width=console)
    chat_message = " ".join(chat)
    try:
        client, model_name = get_llm(provider=provider, api_key=api_key, model=model)
        print_header(console=rich_console, model=model_name, provider=provider)
        system_message = setup_system_message(message=system)
        chat_session(
            client=client,
            console=rich_console,
            system_message=system_message,
            stream=stream,
            panel=border,
            chat_message=chat_message,
            avatar=avatar,
        )
    except KeyboardInterrupt as ki:
        raise click.exceptions.Exit(code=0) from ki


if __name__ == "__main__":
    cli()
