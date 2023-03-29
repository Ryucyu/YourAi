import openai

from YourAi.settings import OPENAI_KEY

openai.api_key = OPENAI_KEY


def ask_gpt(message):
    rsp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    resp = rsp.get("choices")[0]["message"]["content"]
    return resp

