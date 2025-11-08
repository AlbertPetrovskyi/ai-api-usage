import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio

load_dotenv()

GEMINI_API_KEY = os.getenv("AISTUDIO_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("AISTUDIO_API_KEY not found in environment variables or .env file.")

MODEL = "gemini-1.5-pro-latest"

PROMPT = """Write a short poem about the moon."""

async def generate():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(MODEL)
    except Exception as e:
        print(f"Error configuring GenerativeAI: {e}")
        return

    reasoning_prompt = f"""Please think step-by-step to fulfill the following request.
First, explain your reasoning process or plan clearly.
Then, provide the final content.

Request: {PROMPT}
"""

    print(f"Generating content based on:\n---\n{PROMPT}\n---\n")
    print("Gemini Output:\n")

    try:
        response_stream = await model.generate_content_async(
             reasoning_prompt,
             stream=True,
        )

        async for chunk in response_stream:
            if hasattr(chunk, 'text'):
                print(chunk.text, end="", flush=True)

        print()

    except Exception as e:
        print()
        error_message = str(e)
        if hasattr(e, 'message'):
             error_message = e.message
        print(f"\nAn error occurred during generation: {error_message}")


if __name__ == "__main__":
    try:
        asyncio.run(generate())
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")