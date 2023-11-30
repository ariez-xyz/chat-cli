#!venv/bin/python

import openai
import sys
from openai import OpenAI

client = OpenAI()
HISTFILE='chat-cli-history'

if len(sys.argv) < 3 or sys.argv[1] not in ["chat", "reply"]:
    print("Need a mode (chat, reply) and an input string.")
    exit(1)

mode = sys.argv[1]
message = " ".join(sys.argv[2:])

if mode == "chat": # Start a new chat
    messages = [ 
        {"role": "system", "content": "You are a helpful assistant."}, 
        {"role": "user", "content": message}, 
    ]
elif mode == "reply": # Append to history
    with open(HISTFILE, 'r') as f:
        messages = eval(f.readline())
        messages += [ {"role": "user", "content": message} ]


with open(HISTFILE, 'w') as f:
    f.write(repr(messages))

