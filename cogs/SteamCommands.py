from discord import channel, client
from discord.ext.commands import Cog, BucketType, command, cooldown, errors
from discord.ext import commands
from discord.ext.commands.errors import MissingRole
import steam
from steam import client

steam.monkey.patch_minimal()

client.SteamClient.anonymous_login()


class SteamCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="ready")
    async def ready(self, ctx):
        await ctx.send("You are logged into Steam.")


def setup(bot):
    bot.add_cog(SteamCommands(bot))
