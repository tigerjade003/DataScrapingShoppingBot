import asyncio
import discord
import threading
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = os.getenv("USER_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
loop = asyncio.new_event_loop()

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

async def notify(message: str):
    channel = discord.utils.get(client.get_all_channels(), name="bot-test")
    if channel:
        await channel.send(message)
    else:
        print("Channel #bot-test not found!")

def check_event(name, price, goal):
    print(name)
    print(price)
    print(goal)
    if price < goal:
        asyncio.run_coroutine_threadsafe(
            notify(f"{name} is now ${str(price)}! Your goal price was ${str(float(goal))}."),
            loop
        )

def start_bot():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(BOT_TOKEN))

# Start bot in background thread when imported
thread = threading.Thread(target=start_bot, daemon=True)
thread.start()