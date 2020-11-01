from discord.ext.commands import Cog, BucketType, command, cooldown


class BotCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @cooldown(1, 10, BucketType.user)
    async def bob(self, ctx):
        await ctx.send("I am bob. I am male.")

    @command()
    @cooldown(1, 10, BucketType.user)
    async def sandy(self, ctx):
        await ctx.send("Wheres MY fucking content?")

    @command(aliases=["kev"])
    @cooldown(1, 10, BucketType.user)
    async def kevin(self, ctx):
        await ctx.send("You wanna know whats hard?")

    @command()
    @cooldown(1, 10, BucketType.user)
    async def will(self, ctx):
        await ctx.send("So drinks this weekend?")

    @command()
    @cooldown(1, 10, BucketType.user)
    async def alan(self, ctx):
        await ctx.send("ALAN IS A FUCKING PIECE OF SHIT CUNT, IMAGINE BEING BAD AT VALORANT OMEGALUL")

    @command()
    @cooldown(1, 10, BucketType.user)
    async def benson(self, ctx):
        await ctx.send("I want halal")

    @command()
    @cooldown(1, 10, BucketType.user)
    async def sgrug(self, ctx):
        await ctx.send("Ahhh that's so ass cancer this tumorous fucking cunt support man bro fuck this game. Soooo cancer. Fucking loser, at least he is 1-3, you're gonna fucking lose the game dude. Fucking aids........ Just gotta not push lane this alistar has a hard-on for me cause his parents don't love him so he has to love someone else, damn.")

    @command()
    @cooldown(1, 10, BucketType.user)
    async def ivan(self, ctx):
        await ctx.send("This kids dogshit.")

    @command()
    @cooldown(1, 10, BucketType.user)
    async def jason(self, ctx):
        await ctx.send("You wanna do my hw for me?")

    @command()
    @cooldown(1, 10, BucketType.user)
    async def hassan(self, ctx):
        await ctx.send("ff shitters")


def setup(bot):
    bot.add_cog(BotCommands(bot))
