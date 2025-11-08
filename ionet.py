import requests
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("IONET_API_KEY")
MODEL = "deepseek-ai/DeepSeek-R1"
request = input("How can I help you?\n")

url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

data = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": request
        }
    ],
}

response = requests.post(url, headers=headers, json=data)
data = response.json()
# pprint(data)

text = data['choices'][0]['message']['content']
print(text.split('</think>\n\n')[1])
