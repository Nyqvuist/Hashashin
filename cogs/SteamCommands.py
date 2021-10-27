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

    @command(help="Search engine for the steam page.", brief="Search Steam Games.", pass_context=True)
    async def search(self, ctx, *, game):
        gres = requests.get(
            "https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        gdata = gres.json()
        # for x in gdata["applist"]["apps"]:
        # pattern = re.compile(r"{}".format(game))
        # matches = pattern.finditer(gdata["applist"]["apps"])
        # for match in matches:
        # print(match)

        # Finding game name and giving appID a variable.

        for x in gdata["applist"]["apps"]:
            if (x["name"] == game.title()):
                vgame = x["name"]
                appID = (x["appid"])

        # API request to then get game details using appID.

        gsres = requests.get(
            "https://store.steampowered.com/api/appdetails/?appids={}&l=english".format(appID))
        gsdata = gsres.json()

        # Remove html content from description and notice.
        cleanr = re.compile('<.*?>')

        def cleanhtml(raw_html):
            cleantext = re.sub(cleanr, '', raw_html)
            return cleantext

        # Accessing data dictionary and assigned them values.

        appdetails = gsdata.get("{}".format(appID)).get("data")
        notice = appdetails.get("legal_notice")
        description = appdetails.get("short_description")

        # Displaying all information through discord bot.

        embed = discord.Embed(
            title=appdetails["name"],
            url="https://store.steampowered.com/app/{}/".format(appID),
            description=cleanhtml(description),
            color=discord.Color.random()
        )

        embed.set_image(url=appdetails["header_image"])

        # If statement to check if game has a legal notice or not.

        if appdetails.get("legal_notice") not in appdetails.values() or appdetails.get("legal_notice") == None:
            embed.set_footer(text="")
        else:
            embed.set_footer(text=str(cleanhtml(notice))[:180])

        # Adding multiple devs to developer field.

        dev = ", ".join([str(item)
                         for item in appdetails.get("developers")])
        embed.add_field(name="Developers: ",
                        value=dev, inline=True)

        # Checking if game is free to display Free instead of Price.

        if appdetails["is_free"] == True:
            embed.add_field(name="Price: ", value="Free", inline=False)
        else:
            embed.add_field(
                name="Price: ", value=appdetails.get("price_overview")["final_formatted"], inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SteamCommands(bot))
