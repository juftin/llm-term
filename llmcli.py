"""
LLM CLI
"""

import openai
import os
import rich.traceback
from datetime import datetime, timezone
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

rich.traceback.install(show_locals=True)

__application__ = "llm-cli"
__version__ = "0.1.0"
gpt_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
console = Console()


def main():
    """
    LLM CLI
    """

    console.print(
        Panel(
            f"[bold red]{__application__} is a command line interface for OpenAI's Chat API[/bold red]",
            title=f"[blue bold]{__application__} v{__version__}[/blue bold]",
            subtitle=f"[yellow bold]{gpt_model}[/yellow bold]",
            style="green bold",
            expand=False,
        ),
    )
    console.print("")

    try:
        openai.api_key = os.environ["OPENAI_API_KEY"]
    except KeyError:
        console.print(
            "You must set the OPENAI_API_KEY environment variable", style="red"
        )
        exit(1)

    now_utc = datetime.now(timezone.utc)
    setup = f"""
    You are a helpful AI assistant named {__application__}, built by OpenAI and based on 
    the model {gpt_model}. Help the user by responding to their request, the output should 
    be concise and always written in markdown. Ensure that all code blocks have the correct 
    language tag.
    
    The current date and time at the start of this conversation is  
    {datetime.now()} {now_utc.astimezone().tzinfo.tzname(now_utc)}.
    """
    system_message = os.getenv("OPENAI_SYSTEM_MESSAGE", setup)
    messages = [{"role": "system", "content": system_message}]

    while True:
        try:
            text = Prompt.ask("🧑", console=console)
            console.print("")
        except (KeyboardInterrupt, EOFError):
            break
        if not text:
            continue
        messages.append({"role": "user", "content": text})
        try:
            response = openai.ChatCompletion.create(
                model=gpt_model, messages=messages, stream=True
            )
        except KeyboardInterrupt:
            break
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
        console.print("")
        messages.append({"role": "assistant", "content": complete_message})


if __name__ == "__main__":
    main()
