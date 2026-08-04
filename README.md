# HAAA: HOW ABOUT ASK AI?

**English | [中文](README_zh.md)**

A small command line AI assistant tool built with Python and [uv](https://docs.astral.sh/uv/).

Ask questions directly from your terminal. Powered by an OpenAI-compatible API.

## Features

- Ask questions with a single command: `haaa "your question"`
- Manages multiple model configurations (API URL / API KEY / model name)
- Set a default model and switch between models easily
- System prompt tuned for concise, honest CLI answers
- Uses streaming-less requests with thinking & high reasoning effort

## Usage

```bash
# ask a question
uv run main.py "what is the weather today?"
```

> **First time using HAAA?** Run `uv run main.py` (no arguments) or `uv run main.py help` to see the full usage. You'll need to add your first model first:
>
> ```bash
> uv run main.py add --url <API_URL> --key <API_KEY> --name <model-name>
> uv run main.py use 0
> ```
>
> Then you can start asking questions. Unknown options or missing arguments will also print the help screen.

## Model Management

Manage your AI model configurations (any OpenAI-compatible API) directly from the command line:

```bash
# list all saved models
uv run main.py list

# show the current default model
uv run main.py show

# add a model (URL / API KEY / model name)
uv run main.py add --url https://api.example.com/v1/chat/completions --key sk-xxxx --name model-name

# delete a model by its index (see `list` output)
uv run main.py delete 0

# set the model at index as default
uv run main.py use 0

# show this help
uv run main.py help
```

> The first argument `list` / `show` / `add` / `delete` / `use` / `help` triggers the management mode; any other text is treated as a question to ask.

## Configuration

### Model list (`.models`)

Each model takes 3 lines: `API_URL`, `API_KEY`, `model_name`.

```
https://api.example.com/v1/chat/completions
sk-xxxx
model-name
```

### Default model (`.default_model`)

Stores the currently selected model, same 3-line format:
`API_URL`, `API_KEY`, `model_name`.

## Project Structure

```
├── main.py          # CLI entry: management commands + sends your question to the API
├── data.py          # model_data class: API URL / KEY / model + system prompt
├── dataManager.py   # model list management (.models / .default_model)
└── pyproject.toml   # project metadata & dependencies
```

## Todo

- [ ] model list and translate
- [ ] ask model and translation model
- [ ] ask with arguments
- [ ] button of token details
- [ ] set limit of token usage

---

It's my first personal Python project.
Welcome to star, fork, PR!
