import discord
from discord.ext.commands import Cog
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot


class BotCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bob(self, ctx):
        await ctx.send("Loves making people throw up.")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sandy(self, ctx):
        await ctx.send("I bathe in BBT.")

    @commands.command(aliases=["kev"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kevin(self, ctx):
        await ctx.send("Gay.")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def will(self, ctx):
        await ctx.send("So drinks this weekend?")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def alan(self, ctx):
        await ctx.send("Wanna see my highlights?")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def benson(self, ctx):
        await ctx.send("Boosted Plat.")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sgrug(self, ctx):
        await ctx.send("Ahhh that's so ass cancer this tumorous fucking cunt support man bro fuck this game. Soooo cancer. Fucking loser, at least he is 1-3, you're gonna fucking lose the game dude. Fucking aids........ Just gotta not push lane this alistar has a hard-on for me cause his parents don't love him so he has to love someone else, damn.")


def setup(bot):
    bot.add_cog(BotCommands(bot))
