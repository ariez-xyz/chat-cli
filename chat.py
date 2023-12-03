#!venv/bin/python

import sys
from datetime import datetime
from openai import OpenAI

SYS_PROMPT='You are a helpful assistant.\nBe very concise. Your answers should fit within a single paragraph, unless explicitly asked for more.\nAssume that User has a strong technical background. \nAnswer to the best of your ability. This is very important to User\'s career.'

HISTDIR='history/' # dir to save chat histories to
LAST_CHAT_FILE='history/lastchat' # remembers which file contains the most recent chat.

def run(mode, message):
    histfile = ""

    try:
        client = OpenAI()

        if mode == "chat": # Start a new chat
            date_str = datetime.now().strftime("%d-%m-%y-%H:%M:%S")
            histfile = HISTDIR + date_str
            messages = [ 
                {"role": "system", "content": SYS_PROMPT}, 
                {"role": "user", "content": message}, 
            ]
        elif mode == "reply": # Append to history
            with open(LAST_CHAT_FILE, 'r') as f:
                histfile = f.readline().strip()
            with open(histfile, 'r') as f:
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
        print()

    except KeyboardInterrupt:
        print("\nInterrupted.")

    finally:
        with open(LAST_CHAT_FILE, 'w') as f:
            f.write(histfile)
        with open(histfile, 'w') as f:
            f.write(repr(messages + [ {"role": "assistant", "content": res} ]))

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ["chat", "reply"]:
        print("Need a mode (chat, reply) and an input string.")
        exit(1)

    mode = sys.argv[1]
    message = " ".join(sys.argv[2:])

run(mode, message)
