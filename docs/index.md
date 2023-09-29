# llm-term

Chat with OpenAI's GPT models directly from the command line.

<p align="center">
<img width="600" alt="image" src="https://github.com/juftin/llm-term/assets/49741340/4233a9a7-dd24-44c3-b67d-5d13b80c1f89">
</p>

[![PyPI](https://img.shields.io/pypi/v/llm-term?color=blue&label=🤖%20llm-term)](https://github.com/juftin/llm-term)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/llm-term)](https://pypi.python.org/pypi/llm-term/)
[![GitHub License](https://img.shields.io/github/license/juftin/llm-term?color=blue&label=License)](https://github.com/juftin/llm-term/blob/main/LICENSE)
[![Black Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)]()
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-lightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg)](https://gitmoji.dev)

<details>
<summary>Screen Recording</summary>
<video controls>
  <source src="https://user-images.githubusercontent.com/49741340/270871763-d872650e-bceb-4da3-8bc6-3e079d55e5a3.mov" type="video/mp4">
  Your browser does not support the video tag.
</video>
</details>

## Installation

```bash
pipx install llm-term
```

## Usage

Then, you can chat with the model directly from the command line:

```shell
llm-term
```

Make sure you have an OpenAI API key set as an environment variable
(this can also set via the `--api-key` / `-k` flag in the CLI):

```shell
export OPENAI_API_KEY="xxxxxxxxxxxxxx"
```

Optionally, you can set a custom model. llm-term defaults
to `gpt-3.5-turbo` (this can also set via the
`--model` / `-m` flag in the CLI):

```shell
export OPENAI_MODEL="gpt-4"
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
export OPENAI_SYSTEM_MESSAGE="You are a helpful assistant who talks like a pirate."
```
