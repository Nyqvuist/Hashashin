import discord
import logging
import typing
import os
import youtube_dl
import asyncio

from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
from discord.utils import get
from discord.errors import ClientException
from discord.ext.commands import Cog


load_dotenv()

Discord_token = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="$")

client = discord.Client()


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command(
    help="The Yin to my Yang"
)
async def ping(ctx):
    await ctx.send("pong")

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(Discord_token)
