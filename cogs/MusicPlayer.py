import discord
import os

from discord.ext.commands import Cog, Bot, command
from discord.utils import get

client = discord.Client()
bot = Bot(command_prefix="$")


class MusicPlayer(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = client

    @command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        if channel:
            await channel.connect()

    @join.error
    async def join_error(self, ctx, exc):
        if isinstance(exc, AttributeError):
            await ctx.send("You have to be connected to add Hashashin!")

    @command(pass_context=True, aliases=["disconnect"])
    async def leave(self, ctx):
        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.voice_client.disconnect(force=True)

    @leave.error
    async def leave_error(self, ctx, exc):
        if isinstance(exc.original, AttributeError):
            await ctx.send("Hashashin is not in a channel!")

    @command(pass_context=True)
    async def play(self, ctx, url: str):
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

    @command(pass_context=True)
    async def pause(self, ctx):
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("Music has been paused.")
        else:
            await ctx.send("There is no music playing.")

    @command(pass_context=True)
    async def resume(self, ctx):

        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("Music has resumed!")
        else:
            await ctx.send("Music is not paused.")

    @command(pass_context=True)
    async def stop(self, ctx):

        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_playing():
            vc.stop()
            await ctx.send("Music has been stopped.")
        else:
            await ctx.send("No music playing, failed to stop.")


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
