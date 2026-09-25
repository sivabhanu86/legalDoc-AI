import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv("backend/.env", override=True)


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(prompt):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
def stream_answer(prompt):
    stream = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        stream=True
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content

        if content:
            yield content