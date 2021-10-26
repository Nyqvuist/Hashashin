from discord import channel, client
from discord.ext.commands import Cog, BucketType, command, cooldown, errors
from discord.ext import commands
from discord.ext.commands.errors import MissingRole
import steam
from steam.webapi import WebAPI
import os
import requests
from discord import Embed
import re
import discord


STEAM_KEY = os.getenv("STEAM_KEY")

api = WebAPI(key=STEAM_KEY)


class SteamCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
    # Basic search function for steam API for appID

    @command(pass_context=True)
    async def search(self, ctx, *, message):
        gres = requests.get(
            "https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        gdata = gres.json()
        # for x in gdata["applist"]["apps"]:
        # pattern = re.compile(r"{}".format(message.title()))
        # matches = pattern.finditer(x["name"])
        # for match in matches:
        # print(match)
        # await ctx.send(match)

        # Finding game name and giving appID a variable.
        for x in gdata["applist"]["apps"]:
            if (x["name"] == message.title()):
                game = x["name"]
                appID = (x["appid"])

        # API request to then get game details using appID.
        gsres = requests.get(
            "https://store.steampowered.com/api/appdetails/?appids={}".format(appID))
        gsdata = gsres.json()

        # Accessing data sub-dictionary for all appdetails.
        appdetails = gsdata["{}".format(appID)]["data"]

        # Displaying all information through discord bot.
        embed = discord.Embed(
            title=appdetails["name"],
            description=appdetails["short_description"],
            color=discord.Color.green()
        )

        embed.set_image(url=appdetails["header_image"])

        # Try block to pass an exception if game has no legal_notice.
        try:
            embed.set_footer(text=appdetails["legal_notice"][:185])
        except discord.errors.ClientException:
            pass
        except:
            print("!ERROR!")

        # Adding multiple devs to developer field.
        dev = ", ".join([str(item) for item in appdetails["developers"]])

        embed.add_field(name="Developers: ",
                        value=dev, inline=True)

        embed.add_field(
            name="Price: ", value=appdetails["price_overview"]["final_formatted"], inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SteamCommands(bot))
