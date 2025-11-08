import aiohttp
import json
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '' # @BotFather

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

API_URL = "https://api.sambanova.ai/v1/chat/completions"
API_KEY = ""  # SambaNova API
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "DeepSeek-R1" # Model
thinking_cache = {}

async def get_ai_response(user_message: str) -> tuple:
    payload = {
        "stream": False,
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are regular assistant"  # System Instructions
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=payload, headers=HEADERS) as response:
                if response.status == 200:
                    response_json = await response.json()
                    full_response = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
                    thinking_match = re.search(r'<think>(.*?)</think>', full_response, re.DOTALL)
                    thinking_text = thinking_match.group(1).strip() if thinking_match else None
                    clean_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()
                    
                    return clean_response, thinking_text
                else:
                    error_text = await response.text()
                    return f"API Error: {response.status} - {error_text}", None
    except Exception as e:
        return f"Error: {str(e)}", None

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Hi! I'm AI. Ask me and will try to answer!")

@dp.message()
async def handle_message(message: Message):
    user_text = message.text
    await bot.send_chat_action(message.chat.id, "typing")
    ai_response, thinking = await get_ai_response(user_text)
    if thinking:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="Reason", 
            callback_data=f"show_thinking_{message.message_id}"
        ))
        keyboard = builder.as_markup()
        sent_message = await message.answer(ai_response, reply_markup=keyboard)
        thinking_cache[f"{message.message_id}_{sent_message.message_id}"] = thinking
    else:
        await message.answer(ai_response)

@dp.callback_query(lambda c: c.data.startswith('show_thinking_'))
async def process_thinking_callback(callback_query: types.CallbackQuery):
    message_id = callback_query.data.split('_')[2]
    cache_key = f"{message_id}_{callback_query.message.message_id}"

    thinking_text = thinking_cache.get(cache_key)
    
    if thinking_text:
        await callback_query.message.answer(
            f"Reason:\n\n{thinking_text}",
            reply_to_message_id=callback_query.message.message_id
        )
        await callback_query.answer()
    else:
        await callback_query.answer("No reason found.", show_alert=True)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())