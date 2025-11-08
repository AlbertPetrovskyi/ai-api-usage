import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("TUNESTUDIO_API_KEY")
MODEL = "anthropic/claude-3.5-sonnet"
def chat_with_model():
    stream = True
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json",
    }

    print(f"Chat with {MODEL} (by Kavinsky)\nFor exit write 'exit'\n")

    messages = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        data = {
            "temperature": 0.8,
            "messages": messages,
            "model": MODEL,
            "stream": stream,
            "frequency_penalty": 0,
            "max_tokens": 8192
        }

        response = requests.post(url, headers=headers, json=data, stream=True)
        
        if response.status_code == 200:
            print(f"{MODEL}: ", end="", flush=True)
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        chunk = line[6:]
                        if chunk != "[DONE]":
                            chunk_json = json.loads(chunk)
                            content = chunk_json['choices'][0]['delta'].get('content', '')
                            print(content, end="", flush=True)
            print()
            messages.append({"role": "assistant", "content": content})
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    chat_with_model()