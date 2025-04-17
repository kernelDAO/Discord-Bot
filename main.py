import discord
import os

from src import bot
from config import TOKEN

os.system("cls")

print("""
  _                            _ _____          _____  
 | |                          | (____ \\   /\\   / ___ \\ 
 | |  _ ____  ____ ____   ____| |_   \\ \\ /  \\ | |   | |
 | | / ) _  )/ ___)  _ \\ / _  ) | |   | / /\\ \\| |   | |
 | |< ( (/ /| |   | | | ( (/ /| | |__/ / |__| | |___| |
 |_| \\_)____)_|   |_| |_|\\____)_|_____/|______|\\_____/ 
                  DISCORD SOFTWARE
Open-source and free software made by: t.me/kerneldrops
""")

print("Enter \"1\" to launch the Discord bot.")
start = input()
if start == "1":
    print("Started!")
    try:
        if TOKEN:
            bot.client.run(TOKEN, log_handler=None)
        else:
            print("❌ Token is not defied in config.py")
    except discord.LoginFailure as e:
        print(f"❌ Login error: {e}")
    except Exception as e:
        print(f"❌ Runtime error: {e}")