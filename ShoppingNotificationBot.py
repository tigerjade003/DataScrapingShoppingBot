import asyncio
import discord
from discord import app_commands
import threading
import os
from dotenv import load_dotenv
import getOpenBox
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
    await interaction.response.defer()
    sku = link.split("/sku/")[1].split("/")[0]
    name, prices = getOpenBox.get_data(link, sku)

    if goal_price is None:
        goal_price = prices[3]  # regular price as default
    print("HI")
    db.insert(url=link, goalPrice=goal_price)
    await interaction.followup.send(f"Tracking **{name}** — will alert when below ${goal_price}!")

@tree.command(name="list_pricewatches", description="List all your active price watches")
async def list_pricewatches(interaction: discord.Interaction):
    products = db.get_all_products()

    if not products:
        await interaction.response.send_message("You have no active price watches.")
        return

    lines = []
    for p in products:
        name = p["name"] or "Unknown Product"
        fair = p["openbox_fair"] or "N/A"
        good = p["openbox_good"] or "N/A"
        excellent = p["openbox_excellent"] or "N/A"
        regular = p["price"] or "N/A"
        wanted = p["wanted_price"] or "N/A"
        url = p["url"] or ""
        sku = p["sku"]

        lines.append(
            f"**{name}** — SKU: `{sku}`\n"
            f"  Fair: ${fair} | Good: ${good} | Excellent: ${excellent} | Regular: ${regular}\n"
            f"  Goal: ${wanted}\n"
            f"  {url}"
        )

    message = "\n\n".join(lines)
    if len(message) <= 2000:
        await interaction.response.send_message(message)
    else:
        chunks = []
        current_chunk = ""
        for line in lines:
            if len(current_chunk) + len(line) + 2 > 2000:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += ("\n\n" if current_chunk else "") + line
        if current_chunk:
            chunks.append(current_chunk)

        await interaction.response.send_message(chunks[0])
        for chunk in chunks[1:]:
            await interaction.followup.send(chunk)

async def notify(message: str):
    channel = discord.utils.get(client.get_all_channels(), name="bot-test")
    if channel:
        await channel.send(message)
    else:
        print("Channel #bot-test not found!")

def check_event(name, price, goal, url):
    if price < goal:
        asyncio.run_coroutine_threadsafe(
            notify(f"{name} is now ${str(price)}! Your goal price was ${str(float(goal))}. URL: {url}"),
            loop
        )

def start_scraper():
    db.init_db()
    while True:
        db.refresh_all()
        import time
        time.sleep(db.REFRESH_INTERVAL)

if __name__ == "__main__":
    scraper_thread = threading.Thread(target=start_scraper, daemon=True)
    scraper_thread.start()

    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(BOT_TOKEN))