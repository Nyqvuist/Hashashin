import tanjun
import hikari
import steam
from steam.webapi import WebAPI
from nltk.tokenize import sent_tokenize
import datetime
import difflib
import re
import os
import requests
import nltk
import asyncio
from hashashin.search import SteamSearch

nltk.download('punkt')

STEAM_KEY = os.environ.get("STEAM_KEY")

api = WebAPI(key=STEAM_KEY)


component = tanjun.Component()


@component.with_slash_command
@tanjun.with_str_slash_option("game", "The name of the game.")
@tanjun.as_slash_command("search", "Search for a game.")
async def command_search(ctx: tanjun.abc.Context, game: str) -> None:

    results = await SteamSearch(game)

    appID = results[0]

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

    embed = hikari.Embed(
        title=appdetails["name"],
        url="https://store.steampowered.com/app/{}/".format(appID),
        description=cleanhtml(description),
        color=hikari.Color(0x00FFFF)
    )
    embed.set_image(appdetails["header_image"])
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

    await ctx.respond(embed)


@component.with_slash_command
@tanjun.with_str_slash_option("id", "Steam Profile Name")
@tanjun.with_str_slash_option("game", "The name of the game.")
@tanjun.as_slash_command("achieve", "Players Achievements")
async def player_achievement(ctx: tanjun.abc.Context, game: str, id: str) -> None:

    results = await SteamSearch(game)

    appID = results[0]
    name = results[1]

    idata = (requests.get("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={}".format(
        STEAM_KEY) + "&vanityurl={}".format(id))).json()

    if idata["response"].get("steamid") not in idata["response"].values():
        await ctx.respond("There is no match for this ID.")
    else:
        real_id = idata["response"]["steamid"]

        adata = (requests.get("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?appid=" +
                              str(appID) + "&key=" + str(STEAM_KEY) + "&steamid=" + str(real_id))).json()

        if adata["playerstats"].get("error") in adata["playerstats"].values():
            await ctx.respond("This profile is not public.")
        else:

            stats = adata["playerstats"]

            if stats.get("achievements") not in stats.values():
                await ctx.respond(name + " does not have achievements.")
            else:
                achievements = adata["playerstats"]["achievements"]
                alist = [x for x in achievements
                         if x["achieved"] == 1]

                await ctx.respond(id + " has completed " + str(len(alist)) + " out of " + str(len(achievements)) + " achievements in " + name + ".")


@component.with_slash_command
@tanjun.with_str_slash_option("game", "The name of the game.")
@tanjun.as_slash_command("update", "Game Updates.")
async def game_updates(ctx: tanjun.abc.Context, game: str) -> None:

    results = await SteamSearch(game)

    appID = results[0]

    updata = (requests.get(
        "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={}".format(appID))).json()

    cleanr = re.compile(
        f'<.*?>|{{.*?}}|\[img\].+\[/img\]|\[.*?\]')

    def cleanhtml(raw_html):
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    item = updata["appnews"]["newsitems"]
    contents = cleanhtml(item[0]["contents"])

    # Tokenizes sentence to limit the amt of sentences displayed.

    scontents = sent_tokenize(contents)
    contents = " ".join([str(item) for item in scontents[:5]])

    url = item[0]["url"]
    url = url.replace(" ", "")

    embed = hikari.Embed(
        title=item[0]["title"],
        url=url,
        description=contents,
        color=hikari.Color(0x454B1B)
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

    await ctx.respond(embed=embed)


@component.with_slash_command
@tanjun.with_str_slash_option("game", "The name of the game.")
@tanjun.as_slash_command("count", "Number of Players")
async def count(ctx: tanjun.abc.Context, game: str) -> None:
    results = await SteamSearch(game)

    appID = results[0]
    name = results[1]

    codata = (requests.get(
        "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={}".format(appID))).json()

    player_count = codata["response"]["player_count"]

    await ctx.respond("There are currently " + "`{}`".format(player_count) + " playing {}.".format(name))


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
