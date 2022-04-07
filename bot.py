import hikari
import tanjun
import os
import logging
from dotenv import load_dotenv
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pathlib import Path


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = hikari.GatewayBot(DISCORD_TOKEN)

client = tanjun.Client.from_gateway_bot(
    bot, declare_global_commands=True, mention_prefix=True)


@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    print("Hashashin is online!")

client.load_modules(*Path("./modules").glob("*.py"))

bot.run()

