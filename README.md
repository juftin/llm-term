# LLM-CLI

Chat with OpenAI's GPT models directly from the command line.

<p align="center">
<img width="600" alt="image" src="https://github.com/juftin/llm-cli/assets/49741340/77dd0f74-6beb-4286-bba3-359b46ac0dd0">
</p>

## Installation

```bash
pipx install git+https://github.com/juftin/llm-cli
```

## Usage

Make sure you have an OpenAI API key set as an environment variable:

```shell
export OPENAI_API_KEY="xxxxxxxxxxxxxx"
```

Then, you can chat with the model directly from the command line:

```shell
llm-cli
```

Optionally, you can set a custom model. LLM-CLI defaults
to `gpt-3.5-turbo`:

```shell
export OPENAI_MODEL="gpt-4"
```

<details>
<summary>Screen Recording</summary>

https://user-images.githubusercontent.com/49741340/267864605-5c29a31b-4ea9-477b-aa91-a3c06e9f0477.mov

</details>
