# chat-cli

Minimal ChatGPT CLI.

## Usage

```fish
# run_cli.fish
set -x OPENAI_API_KEY "$key"
chat.py $argv
```

I've added two scripts to my path so that I can call ChatGPT just using `chat` as a command, and `reply` to continue a conversation instead of starting a new one.

```fish
cd /home/ariez/chat-cli/
run_cli.fish chat $argv
```
