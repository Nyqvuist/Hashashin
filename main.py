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

load_dotenv()

Discord_token = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="$")

client = discord.Client()


@bot.event
async def on_ready():
    print("Hashashin is online.")


@bot.command(pass_context=True, aliases=["join"])
async def hassan(ctx, channel: discord.VoiceChannel = None):
    channel = ctx.message.author.voice.channel
    await channel.connect(timeout=60.0)


@hassan.error
async def hassan_error(ctx, exc):
    if isinstance(exc.original, AttributeError):
        await ctx.send("You have to be connected to add Hashashin!")


@bot.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send("bye")
    await bot.process_commands(message)


@bot.command()
async def bottles(ctx, amount: typing.Optional[int] = 99, *, liquid="beer"):
    await ctx.send('{} bottles of {} on the wall!'.format(amount, liquid))


@bot.command(
    help="Looks like someone needs help."
)
async def print(ctx, *args):
    response = ""

    for arg in args:
        response = response + "" + arg
    await ctx.send(response)


@bot.command(
    help="He need some milk!"
)
async def ping(ctx):
    await ctx.send("pong")

bot.run(Discord_token)
