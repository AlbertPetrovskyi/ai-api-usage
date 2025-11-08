import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")
API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"

def get_response_stream(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": messages,
        "stream": True
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(data), stream=True)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        yield None
        return

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data: '):
                json_data = decoded_line[len('data: '):]
                if json_data.strip() == '[DONE]':
                    break
                try:
                    chunk = json.loads(json_data)
                    if 'choices' in chunk and len(chunk['choices']) > 0:
                        delta = chunk['choices'][0].get('delta', {})
                        content = delta.get('content', '')
                        yield content
                except json.JSONDecodeError:
                    continue

def main():
    print(f"Chat with {MODEL}")
    messages = []
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Exit")
            break
        
        messages.append({"role": "user", "content": user_input})
        
        assistant_response = []
        print("AI: ", end='', flush=True)
        try:
            for chunk in get_response_stream(messages):
                if chunk is not None:
                    print(chunk, end='', flush=True) 
                    assistant_response.append(chunk)
            print() 
            full_response = ''.join(assistant_response)
            messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(f"\nerror: {str(e)}")

if __name__ == "__main__":
    main()