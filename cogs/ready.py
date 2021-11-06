from discord.ext.commands import Cog


class Ready(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Hashashin is online.")


def setup(bot):
    bot.add_cog(Ready(bot))
