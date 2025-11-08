import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio

load_dotenv()

GEMINI_API_KEY = os.getenv("AISTUDIO_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("AISTUDIO_API_KEY not found in environment variables or .env file.")

MODEL = "gemini-1.5-pro-latest"

async def chat():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(MODEL)
    except Exception as e:
        print(f"Error configuring GenerativeAI: {e}")
        return

    print(f"Using model: {MODEL}")
    print("Type 'exit' to end the chat. I will try to explain my reasoning.")
    print("(Made by Kavinsky)\n\nHi! I'm Gemini. How can I help you today?")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
             print("\nGoodbye! 👋")
             break

        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break

        if not user_input.strip():
            continue

        prompt = f"""Please think step-by-step to answer the following question.
First, explain your reasoning process clearly.
Then, provide the final answer, perhaps marking it like 'Final Answer:'.

User Question: {user_input}
"""

        try:
            print("Gemini: ", end="", flush=True)

            response_stream = await model.generate_content_async(
                 prompt,
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

            print(f"\nAn error occurred: {error_message}")
            print("Please try again or rephrase your question.")

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nChat interrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")