from typing import Counter
from discord import channel, client
from discord.ext.commands import Cog, BucketType, command, cooldown, errors
from discord.ext import commands
from discord.ext.commands.errors import MissingRole
import random

responses = ["It is Certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As i see it, yes.",
             "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again?", "Ask again later.",
             "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Dont count on it.", "My reply is no.",
             "My sources say no.", "Outlook is not good.", "Very doubtful.", "Bro...*what?*", "I think you should get off the internet.",
             "No.",
             ]


class BallCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = responses

    @command(name="8ball")
    @cooldown(1, 5, BucketType.user)
    async def _8ball(self, ctx, message):
        await ctx.send("**Hello {},**".format(ctx.message.author.nick))
        await ctx.send(responses[random.randint(1, len(responses))])


def setup(bot):
    bot.add_cog(BallCommands(bot))
