import asyncio
import discord
from discord import app_commands
import threading
import os
from dotenv import load_dotenv
import constantshoppingupdate
import db

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = os.getenv("USER_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
loop = asyncio.new_event_loop()

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot is online as {client.user}")

@tree.command(name="add_pricewatch", description="Add a price watch for a product")
@app_commands.describe(
    link="The product URL to track",
    goal_price="Optional target price to alert you at"
)
async def add_pricewatch(interaction: discord.Interaction, link: str, goal_price: float = None):
    if goal_price is None:
        goal_price = constantshoppingupdate.get_price(link)
    await interaction.response.send_message(f"Tracking {link} — will alert when below ${goal_price}!")
    db.insert_product(url=link, wanted_price=str(goal_price))
        
    

async def notify(message: str):
    channel = discord.utils.get(client.get_all_channels(), name="bot-test")
    if channel:
        await channel.send(message)
    else:
        print("Channel #bot-test not found!")

def check_event(name, price, goal, url):
    print(name)
    print(price)
    print(goal)
    if price < goal:
        asyncio.run_coroutine_threadsafe(
            notify(f"{name} is now ${str(price)}! Your goal price was ${str(float(goal))}. URL: {url}"),
            loop
        )

def start_bot():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(BOT_TOKEN))

# Start bot in background thread when imported
thread = threading.Thread(target=start_bot, daemon=True)
thread.start()