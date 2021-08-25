from typing import Counter
from discord import channel, client
from discord.ext.commands import Cog, BucketType, command, cooldown, errors
from discord.ext import commands
from discord.ext.commands.errors import MissingRole
from aiohttp import request


class ValorantCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = channel

    @command()
    @cooldown(1, 10, BucketType.user)
    async def leaderboard(self, ctx, args):

        URL = "https://na.api.riotgames.com/val/ranked/v1/leaderboards/by-act/2a27e5d2-4d30-c9e2-b15a-93b8909a442c?size=100&startIndex=0&api_key=RGAPI-41699ae4-4fa1-4a9d-8c9b-d80b20d6b390"

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                await ctx.send(data["gameName":"leaderboardRank"])


def setup(bot):
    bot.add_cog(ValorantCommands(bot))
