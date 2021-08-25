from typing import Counter
from discord.ext.commands import Cog, BucketType, command, cooldown, errors
from discord.ext import commands
from discord.ext.commands.errors import MissingRole


class BotCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Counter = 20

    @command()
    @cooldown(1, 10, BucketType.user)
    async def swear(self, ctx):
        self.Counter += 1
        print(str(self.Counter))
        await ctx.send("Yanyi please stop swearing you now have {} dollars in your swear jar.".format(self.Counter))
        return self.Counter

    @command()
    @cooldown(1, 10, BucketType.user)
    async def count(self, ctx):
        await ctx.send("Yanyi owes {} dollars due to her potty mouth.".format(self.Counter))

    @command()
    @commands.has_role('Commando')
    @cooldown(1, 10, BucketType.user)
    async def oops(self, ctx):
        self.Counter -= 1
        print(str(self.Counter))
        await ctx.send("Yanyi owes {} dollars now. Whoops.".format(self.Counter))
        return self.Counter

    @oops.error
    async def oops_error(self, ctx, exc):
        if isinstance(exc, MissingRole):
            await ctx.send("You are not a Commando to use this command!")


def setup(bot):
    bot.add_cog(BotCommands(bot))
