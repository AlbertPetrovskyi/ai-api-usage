import requests

url = "https://api.langdock.com/anthropic/eu/v1/messages"
payload = {
    "model": "claude-3-7-sonnet-20250219",
    "system": "You are a helpful assistant.",
    "messages": [
        {"role": "user", "content": "Hi, how are you?"}
    ],
    "max_tokens": 8192
}
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer API_KEY"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    response_data = response.json()

    if "content" in response_data:
        print(response_data["content"])
    else:
        print(response_data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)