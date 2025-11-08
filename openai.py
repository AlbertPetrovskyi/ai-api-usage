from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def generate_response(text):
     response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="gpt-3.5-turbo",
        n=1,
        stop=None,
        temperature=0.5
     )
     if response and response.choices:
        print(response.choices[0].message["content"].strip())
     else:
        print("No comments.")

generate_response("Hello!")