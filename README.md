# Bedrock Bot

This project is a basic CLI-based chat bot that uses Bedrock to resolve questions. It can take input from stdin, CLI arguments or interactively when no parameters have been passed.

## Installation

`pip install bedrock-bot`

## Usage

Directly as a chat bot:

```bash
$ bedrock

Hello! I am an AI assistant powered by Amazon Bedrock and using the model Claude-3-Haiku. Enter 'quit' or 'exit' at any time to exit. How may I help you today?
(You can clear existing context by starting a query with 'new>' or 'reset>')

> Hi, what is your name?
My name is Claude.
```

Using CLI arguments:

```bash
$ bedrock "Hi, what is your name?"

Hello! I am an AI assistant powered by Amazon Bedrock and using the model Claude-3-Haiku. Enter 'quit' or 'exit' at any time to exit. How may I help you today?
(You can clear existing context by starting a query with 'new>' or 'reset>')

> Hi, what is your name?
My name is Claude. It's nice to meet you!
```

Using stdin (Note that you can only use this for one-shot questions as input is reserved by your pipe to stdin and is not an interactive TTY any more):

```bash
$ echo "Hi, what is your name?" > input-file

$ cat input-file | bedrock
Hello! I am an AI assistant powered by Amazon Bedrock and using the model Claude-3-Haiku. Enter 'quit' or 'exit' at any time to exit. How may I help you today?
(You can clear existing context by starting a query with 'new>' or 'reset>')

> Hi, what is your name?

My name is Claude. I'm an AI created by Anthropic. It's nice to meet you!                                                         


Note that you can only do one-shot requests when providing input via stdin
```
