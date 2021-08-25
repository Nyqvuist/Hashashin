from typing import Counter
from discord import channel, client
from discord.ext.commands import Cog, BucketType, command, cooldown, errors
from discord.ext import commands
from discord.ext.commands.errors import MissingRole


class BRCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = channel

    @command()
    @cooldown(1, 10, BucketType.user)
    async def vincent(self, ctx):
        if ctx.channel.id != 702025574457278494:
            await ctx.send("You in the wrong channel!")
        else:
            await ctx.send("What is going on?")
        return

    @command()
    @cooldown(1, 10, BucketType.user)
    async def peter(self, ctx):
        await ctx.send("Your ass is mine.")


def setup(bot):
    bot.add_cog(BRCommands(bot))
