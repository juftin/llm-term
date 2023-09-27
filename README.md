# llm-term

Chat with OpenAI's GPT models directly from the command line.

<p align="center">
<img width="600" alt="image" src="https://github.com/juftin/llm-cli/assets/49741340/77dd0f74-6beb-4286-bba3-359b46ac0dd0">
</p>

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

<details>
<summary>Screen Recording</summary>

https://user-images.githubusercontent.com/49741340/267864605-5c29a31b-4ea9-477b-aa91-a3c06e9f0477.mov

</details>
