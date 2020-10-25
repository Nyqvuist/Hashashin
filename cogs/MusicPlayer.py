import discord
import youtube_dl
import os
from discord.ext.commands import Cog
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot


class MusicPlayer(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect(timeout=60.0)

    @join.error
    async def join_error(self, ctx, exc):
        if isinstance(exc.original, AttributeError):
            await ctx.send("You have to be connected to add Hashashin!")

    @commands.command(pass_context=True, aliases=["disconnect"])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(channel.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()

    @leave.error
    async def leave_error(self, ctx, exc):
        if isinstance(exc.original, AttributeError):
            await ctx.send("Hashashin is not in a channel!")


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
