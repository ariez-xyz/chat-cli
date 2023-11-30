#!venv/bin/python

import sys
from openai import OpenAI

HISTFILE='chat-cli-history'
SYS_PROMPT='You are a helpful assistant. Be very concise. Your answers should fit within one to two paragraphs, unless explicitly asked for more. Answer to the best of your ability. This is very important to User\'s career.'

def run(mode, message):
    try:
        client = OpenAI()

        if mode == "chat": # Start a new chat
            messages = [ 
                {"role": "system", "content": SYS_PROMPT}, 
                {"role": "user", "content": message}, 
            ]
        elif mode == "reply": # Append to history
            with open(HISTFILE, 'r') as f:
                messages = eval(f.readline()) # TODO glaring security issue
                messages += [ {"role": "user", "content": message} ]

        stream = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=messages,
                stream=True,
                )

        res = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                res += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)

    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        with open(HISTFILE, 'w') as f:
            f.write(repr(messages + [ {"role": "assistant", "content": res} ]))

if len(sys.argv) < 3 or sys.argv[1] not in ["chat", "reply"]:
    print("Need a mode (chat, reply) and an input string.")
    exit(1)

mode = sys.argv[1]
message = " ".join(sys.argv[2:])

run(mode, message)
