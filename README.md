# llm-term

Chat with LLM models directly from the command line.

<p align="center">
<img width="600" alt="image" src="https://i.imgur.com/1BUegLB.png">
</p>

[![PyPI](https://img.shields.io/pypi/v/llm-term?color=blue&label=🤖%20llm-term)](https://github.com/juftin/llm-term)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/llm-term)](https://pypi.python.org/pypi/llm-term/)
[![GitHub License](https://img.shields.io/github/license/juftin/llm-term?color=blue&label=License)](https://github.com/juftin/llm-term/blob/main/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-lightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg)](https://gitmoji.dev)

<details>
<summary>Screen Recording</summary>

https://user-images.githubusercontent.com/49741340/270871763-d872650e-bceb-4da3-8bc6-3e079d55e5a3.mov

</details>

<h2><a href="https://juftin.com/llm-term">Check Out the Docs</a></h2>

## Installation

```bash
pipx install llm-term
```

## Usage

Then, you can chat with the model directly from the command line:

```shell
llm-term
```

`llm-term` works with multiple LLM providers, but by default it uses OpenAI.
Most providers require extra packages to be installed, so make sure you
read the [Providers](#providers) section below. To use a different provider, you
can set the `--provider` / `-p` flag:

```shell
llm-term --provider anthropic
```

If needed, make sure you have your LLM's API key set as an environment variable
(this can also set via the `--api-key` / `-k` flag in the CLI). If your LLM uses
a particular environment variable for its API key, such as `OPENAI_API_KEY`,
that will be detected automatically.

```shell
export LLM_API_KEY="xxxxxxxxxxxxxx"
```

Optionally, you can set a custom model. llm-term defaults
to `gpt-3.5-turbo` (this can also set via the `--model` / `-m` flag in the CLI):

```shell
export LLM_MODEL="gpt-4"
```

Want to start the conversion directly from the command line? No problem,
just pass your prompt to `llm-term`:

```shell
llm-term show me python code to detect a palindrome
```

You can also set a custom system prompt. llm-term defaults to a reasonable
prompt for chatting with the model, but you can set your own prompt (this
can also set via the `--system` / `-s` flag in the CLI):

```shell
export LLM_SYSTEM_MESSAGE="You are a helpful assistant who talks like a pirate."
```

## Providers

### OpenAI

By default, llm-term uses OpenAI as your LLM provider. The default model is
`gpt-3.5-turbo` and you can also use the `OPENAI_API_KEY` environment variable
to set your API key.

### Anthropic

You can request access to Anthropic [here](https://www.anthropic.com/). The
default model is `claude-2.1`, and you can use the `ANTHROPIC_API_KEY` environment
variable. To use `anthropic` as your provider you must install the `anthropic`
extra.

```shell
pipx install "llm-term[anthropic]"
```

```shell
llm-term --provider anthropic
```

### MistralAI

You can request access to the [MistralAI](https://mistral.ai/)
[here](https://console.mistral.ai/). The default model is
`mistral-small`, and you can use the `MISTRAL_API_KEY` environment variable.

```shell
pipx install "llm-term[mistralai]"
```

```shell
llm-term --provider mistralai
```

### GPT4All

GPT4All is a an open source LLM provider. These models run locally on your
machine, so you don't need to worry about API keys or rate limits. The default
model is `mistral-7b-openorca.Q4_0.gguf`, and you can see what models are available on the [GPT4All
Website](https://gpt4all.io/index.html). Models are downloaded automatically when you first use them.
To use GPT4All as your provider you must install the `gpt4all` extra.

```bash
pipx install "llm-term[gpt4all]"
```

```shell
llm-term --provider gpt4all --model mistral-7b-openorca.Q4_0.gguf
```
