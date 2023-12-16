import os
import openai


def main(messages, model,apikey):
    openai.api_key = apikey

    completion = openai.ChatCompletion.create(
        model= model,
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": messages}
        ]
    )

    return completion['choices'][0]['message']['content']

