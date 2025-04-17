import discord 
from discord.ext import commands
import asyncio
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time

from config import (
    ACTIVE_CHANNELS, ALLOWED_GUILDS,
    REPLY_PROBABILITY, REPLY_TO_REPLY_PROBABILITY,
    MIN_ANSWERS_BEFORE_PAUSE, MAX_ANSWERS_BEFORE_PAUSE,
    MIN_PAUSE_SECONDS, MAX_PAUSE_SECONDS, GM_PROBABILITY
)
from src.gpt import get_gpt_response

executor = ThreadPoolExecutor(max_workers=5)

total_answer_count = 0
pause_until = None
pause_after = random.randint(MIN_ANSWERS_BEFORE_PAUSE, MAX_ANSWERS_BEFORE_PAUSE)

client = commands.Bot(command_prefix="<", self_bot=True, fetch_offline_members=False)

async def get_gpt_response_async(message):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, get_gpt_response, message)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user.name} ({client.user.id})")

    if random.random() < GM_PROBABILITY:
        try:
            with open("gms.txt", "r", encoding="utf-8") as file:
                messages = [line.strip() for line in file if line.strip()]
            
            if not messages:
                print("⚠️ gms.txt is empty.")
                return

            for guild in client.guilds:
                if guild.id in ALLOWED_GUILDS:
                    for channel_id in ACTIVE_CHANNELS:
                        channel = guild.get_channel(channel_id)
                        if channel:
                            message_to_send = random.choice(messages)
                            try:
                                await channel.send(message_to_send)
                                print(f"🌅 GM sent → '{message_to_send}' → #{channel.name} ({guild.name})")
                            except Exception as e:
                                print(f"⚠️ Failed to send GM to #{channel.name}: {e}")

        except Exception as e:
            print(f"⚠️ Error while loading GMs: {e}")
    else:
        print("⏭️ GM not sent — probability check failed")


@client.event
async def on_message(message):
    global total_answer_count, pause_until, pause_after

    if message.author.id == client.user.id:
        return

    if message.guild is None or message.guild.id not in ALLOWED_GUILDS:
        return

    channel_id = getattr(message.channel, 'parent_id', message.channel.id)
    if channel_id not in ACTIVE_CHANNELS:
        return

    now = asyncio.get_event_loop().time()
    if pause_until and now < pause_until:
        print("😴 Bot is on pause — not responding")
        return

    is_reply_to_bot = False
    if message.reference and message.reference.resolved:
        original = message.reference.resolved
        if isinstance(original, discord.Message) and original.author.id == client.user.id:
            is_reply_to_bot = True

    reply_chance = REPLY_TO_REPLY_PROBABILITY if is_reply_to_bot else REPLY_PROBABILITY
    if random.randint(1, 100) > reply_chance:
        print(f"🤫 Skipped — chance failed ({reply_chance}%)")
        return

    try:
        print(f"📨 {message.author}: {message.content}")
        response = await get_gpt_response_async(message.content)

        typing_delay = min(len(response) * 0.05, 6)
        async with message.channel.typing():
            await asyncio.sleep(random.uniform(1.5, 3.0) + typing_delay)
            await message.channel.send(response, reference=message)

        print(f"📤 Replied: '{response}' → #{message.channel.name} ({message.guild.name})")

        total_answer_count += 1
        print(f"🧮 Total replies: {total_answer_count} / {pause_after}")

        if total_answer_count >= pause_after:
            pause_duration = random.randint(MIN_PAUSE_SECONDS, MAX_PAUSE_SECONDS)
            pause_until = now + pause_duration
            total_answer_count = 0
            pause_after = random.randint(MIN_ANSWERS_BEFORE_PAUSE, MAX_ANSWERS_BEFORE_PAUSE)
            end_time = datetime.fromtimestamp(time.time() + pause_duration).strftime('%H:%M:%S')
            print(f"😴 Going on pause for {pause_duration // 60} minutes. New reply limit: {pause_after}")
            print(f"🕒 Pause until: {end_time}")

    except Exception as e:
        print(f"⚠️ Error while responding: {e}")