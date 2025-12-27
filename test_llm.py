from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)

response = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Say hello in one line"}
    ]
)

print(response.choices[0].message.content)