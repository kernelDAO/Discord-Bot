import random
import httpx
from openai import OpenAI
from config import OPENAI_API_KEYS, OPENAI_PROXY, MODEL, BASE_PROMPT
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)

async def get_gpt_response_async(message):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, get_gpt_response, message)

def get_client():
    api_key = random.choice(OPENAI_API_KEYS)

    if OPENAI_PROXY:
        http_client = httpx.Client(proxies=OPENAI_PROXY)
        return OpenAI(api_key=api_key, http_client=http_client)
    else:
        return OpenAI(api_key=api_key)


def get_gpt_response(user_message: str) -> str:
    messages = [
        {"role": "system", "content": BASE_PROMPT},
        {"role": "user", "content": user_message}
    ]

    try:
        client = get_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=150,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Error while generating GPT answer: {e}")
        return ""