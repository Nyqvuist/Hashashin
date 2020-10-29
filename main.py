import discord
import logging
import os

from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()  # Load environment variables

logging.basicConfig(level=logging.INFO)

bot = Bot(command_prefix="$")

client = discord.Client()

# Load all cogs in the cogs directory
for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv("DISCORD_TOKEN"))
