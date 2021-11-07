from discord import channel, client
from discord.ext.commands import Cog, BucketType, command, cooldown, errors
from discord.ext import commands
import steam
from steam.webapi import WebAPI
import os
import requests
import nltk
from discord import Embed
import re
import discord
import difflib
from hashashin.search import SteamSearch
from nltk.tokenize import sent_tokenize
import datetime


nltk.download('punkt')

STEAM_KEY = os.environ.get("STEAM_KEY")

api = WebAPI(key=STEAM_KEY)


class Search(Cog):
    def __init__(self, bot):
        self.bot = bot
    # Basic search function for steam API for appID

    @command(help="Search engine for the steam page.", brief="Search Steam Games.", pass_context=True)
    async def search(self, ctx, *, game):

        # Imported Search function to obtain appID.
        appID = SteamSearch(game)

        # API request to then get game details using appID.
        gsdata = (requests.get(
            "https://store.steampowered.com/api/appdetails/?appids={}&l=english".format(appID))).json()

        # Remove html content from description and notice.
        cleanr = re.compile('<.*?>')

        def cleanhtml(raw_html):
            cleantext = re.sub(cleanr, '', raw_html)
            return cleantext

        # Accessing data dictionary and assigned them values.

        appdetails = gsdata.get("{}".format(appID)).get("data")
        notice = appdetails.get("legal_notice")
        description = appdetails.get("short_description")
        price = appdetails.get("price_overview")

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
            snotice = sent_tokenize(notice)
            notice = " ".join([str(item) for item in snotice[:2]])
            embed.set_footer(text=cleanhtml(notice))

        # Adding multiple devs to developer field.

        dev = ", ".join([str(item)
                         for item in appdetails.get("developers")])
        embed.add_field(name="Developers: ",
                        value=dev, inline=True)

        # Checking if game is free to display Free instead of Price.

        if appdetails["is_free"] == True:
            embed.add_field(name="Price: ", value="Free", inline=False)

        elif price.get("initial_formatted") != "":
            embed.add_field(name="Price: ", value="~~{}~~".format(
                price.get("initial_formatted")) + " " + "**{}**".format(price.get("final_formatted")), inline=False)

        else:
            embed.add_field(
                name="Price: ", value=appdetails.get("price_overview")["final_formatted"], inline=False)

        await ctx.send(embed=embed)

    @command(help="Get Game Updates For Steam Games.", brief="Steam Game News.", pass_context=True)
    async def update(self, ctx, *, game):

        appID = SteamSearch(game)

        updata = (requests.get(
            "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={}".format(appID))).json()

        cleanr = re.compile('<.*?>')

        def cleanhtml(raw_html):
            cleantext = re.sub(cleanr, '', raw_html)
            return cleantext

        item = updata["appnews"]["newsitems"]
        contents = cleanhtml(item[0]["contents"])

        # Tokenizes sentence to limit the amt of sentences displayed.

        scontents = sent_tokenize(contents)
        contents = " ".join([str(item) for item in scontents[:4]])

        embed = discord.Embed(
            title=item[0]["title"],
            url=item[0]["url"],
            description=contents,
            color=discord.Color.random()
        )

        date_time = item[0]["date"]
        date_time = datetime.datetime.fromtimestamp(
            date_time).strftime('%m/%d/%Y')

        embed.add_field(name="Date: ", value=date_time, inline=True)

        if item[0]["author"] != "":

            embed.add_field(name="Author: ",
                            value=item[0]["author"], inline=True)

        else:
            pass

        embed.set_footer(text="Community Announcements.")

        await ctx.send(embed=embed)

    @command(help="Get Number of Players in the Game.", brief="Amount of Players.", pass_context=True)
    async def count(self, ctx, *, game):

        gdata = (requests.get(
            "https://api.steampowered.com/ISteamApps/GetAppList/v2/")).json()

        apps = gdata["applist"]["apps"]
        glist = [x["name"].lower() for x in apps if x["name"]]

        possibilities = glist

        matches = difflib.get_close_matches(
            game.lower(), possibilities, n=1, cutoff=0.3)

        app = [x for x in apps if matches[0] == x["name"].lower()]

        appID = app[0]["appid"]
        name = app[0]["name"]

        codata = (requests.get(
            "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={}".format(appID))).json()

        player_count = codata["response"]["player_count"]

        await ctx.send("There are currently " + "`{}`".format(player_count) + " playing {}.".format(name))

    @command(help="How many completed Achievements.", brief="Completed Achievements.", pass_context=True)
    async def achieve(self, ctx, *, game):

        await ctx.send("Please enter a steamid.")

        def check(m: discord.Message):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        msg = await self.bot.wait_for("message", check=check, timeout=60.0)
        id = msg.content

        gdata = (requests.get(
            "https://api.steampowered.com/ISteamApps/GetAppList/v2/")).json()

        apps = gdata["applist"]["apps"]
        glist = [x["name"].lower() for x in apps if x["name"]]

        possibilities = glist

        matches = difflib.get_close_matches(
            game.lower(), possibilities, n=1, cutoff=0.3)

        app = [x for x in apps if matches[0] == x["name"].lower()]

        appID = app[0]["appid"]
        name = app[0]["name"]

        idata = (requests.get("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={}".format(
            STEAM_KEY) + "&vanityurl={}".format(id))).json()

        real_id = idata["response"]["steamid"]

        adata = (requests.get("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?appid=" +
                              str(appID) + "&key=" + str(STEAM_KEY) + "&steamid=" + str(real_id))).json()

        stats = adata["playerstats"]

        if stats.get("achievements") not in stats.values():
            await ctx.send(name + " does not have achievements.")
        else:
            achievements = adata["playerstats"]["achievements"]
            alist = [x for x in achievements
                     if x["achieved"] == 1]

        await ctx.send(id + " has completed " + str(len(alist)) + " out of " + str(len(achievements)) + " achievements in " + name + ".")


def setup(bot):
    bot.add_cog(Search(bot))
