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
import locale
import random


nltk.download('punkt')

STEAM_KEY = os.environ.get("STEAM_KEY")

api = WebAPI(key=STEAM_KEY)


component = tanjun.Component()


@component.with_slash_command
@tanjun.with_str_slash_option("game", "The name of the game.")
@tanjun.as_slash_command("search", "Search for a game.")
async def command_search(ctx: tanjun.abc.SlashContext, game: str) -> None:

    results = await SteamSearch(game)

    appID = results[0]

    await _game_embed(ctx, appID)



@component.with_slash_command
@tanjun.with_str_slash_option("id", "Steam Profile Name")
@tanjun.with_str_slash_option("game", "The name of the game.")
@tanjun.as_slash_command("achieve", "Players Achievements")
async def player_achievement(ctx: tanjun.abc.SlashContext, game: str, id: str) -> None:

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
async def game_updates(ctx: tanjun.abc.SlashContext, game: str) -> None:

    results = await SteamSearch(game)

    appID = results[0]

    updata = (requests.get(
        "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={}".format(appID))).json()

    cleanr = re.compile(
        f'<.*?>|{{.*?}}|\[img\].+\[/img\]|\[.*?\]')

    def cleanhtml(raw_html):
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    items = updata["appnews"]["newsitems"]

    item = [x for x in items if x["feedlabel"] == "Community Announcements"]

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

    embed.set_footer(text=item[0]["feedlabel"])

    await ctx.respond(embed=embed)


@component.with_slash_command
@tanjun.with_str_slash_option("game", "The name of the game.")
@tanjun.as_slash_command("count", "Number of Players")
async def count(ctx: tanjun.abc.SlashContext, game: str) -> None:
    results = await SteamSearch(game)

    appID = results[0]
    name = results[1]

    gsdata = (requests.get(
        "https://store.steampowered.com/api/appdetails/?appids={}&l=english".format(appID))).json()

    codata = (requests.get(
        "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={}".format(appID))).json()

    check = codata["response"]

    if check.get("player_count") not in check.values():
        await ctx.respond("This game currently does not have players online.")

    else:
        player_count = codata["response"]["player_count"]
        appdetails = gsdata.get("{}".format(appID)).get("data")

        embed = hikari.Embed(
            title=name,
            description="There are currently " + "`{}`".format(player_count) + " playing.",
            color=hikari.Color(0x808080)
        )

        embed.set_thumbnail(appdetails["header_image"])

        await ctx.respond(embed)

@component.with_slash_command
@tanjun.as_slash_command("specials", "Returns Current Steam Specials.")
async def specials(ctx: tanjun.abc.SlashContext) -> None:

    locale.setlocale(locale.LC_ALL,"en_US.UTF-8")

    sdata = (requests.get("http://store.steampowered.com/api/featuredcategories/&l=english")).json()

    specials = sdata["specials"]["items"]

    special1 = specials[0]
    special2 = specials[1]
    special3 = specials[2]
    special4 = specials[3]
    special5 = specials[4]

    embed = hikari.Embed(
        title="Specials",
        url="https://store.steampowered.com/search/?specials=1",
        color=hikari.Color(0xE6E6FA)
    )

    embed.add_field(name = special1["name"], value = "Price: " + locale.currency(float(special1["final_price"]) / 100.0) + "\nDiscount Ends: " + datetime.datetime.fromtimestamp(special1["discount_expiration"]).strftime('%m/%d/%Y'), inline=False)

    embed.add_field(name = special2["name"], value = "Price: " + locale.currency(float(special2["final_price"]) / 100.0) + "\nDiscount Ends: " + datetime.datetime.fromtimestamp(special2["discount_expiration"]).strftime('%m/%d/%Y'), inline=False)

    embed.add_field(name = special3["name"], value = "Price: " + locale.currency(float(special3["final_price"]) / 100.0) + "\nDiscount Ends: " + datetime.datetime.fromtimestamp(special3["discount_expiration"]).strftime('%m/%d/%Y'), inline=False)

    embed.add_field(name = special4["name"], value = "Price: " + locale.currency(float(special4["final_price"]) / 100.0) + "\nDiscount Ends: " + datetime.datetime.fromtimestamp(special4["discount_expiration"]).strftime('%m/%d/%Y'), inline=False)

    embed.add_field(name = special5["name"], value = "Price: " + locale.currency(float(special5["final_price"]) / 100.0) + "\nDiscount Ends: " + datetime.datetime.fromtimestamp(special5["discount_expiration"]).strftime('%m/%d/%Y'), inline=False)

    await ctx.respond(embed)

@component.with_slash_command
@tanjun.with_str_slash_option("genre", "Action, Adventure, RPG, Indie, etc.")
@tanjun.with_str_slash_option("category", "Single-player, Multi-player, PvP, etc.")
@tanjun.as_slash_command("random", "Random game of the given filter.")
async def random_game(ctx: tanjun.abc.SlashContext, category: str, genre: str) -> None:

    categories_list = ["Single-player","Multi-player","PvP", "Online PvP","Co-op","Online Co-op"]
    genres_list = ["Action", "Adventure", "rpg", "Indie", "Racing", "Sports", "Free to Play","Massively Multiplayer", ]

    cmatches = difflib.get_close_matches(
        category.lower(), categories_list, n=1, cutoff=0.3)
    
    gmatches = difflib.get_close_matches(
        genre.lower(), genres_list, n=1, cutoff=0.3)

    await ctx.respond("Your random game is now loading...")

    on = True

    while on:
        results = await _random_game(ctx)
        categories = results[0]
        genres = results[1]
        for x in categories:
            if x["description"].lower() == cmatches[0].lower():
                for y in genres:
                    if y["description"].lower() == gmatches[0].lower():
                        on = False
        
    appID = results[2]

    await _game_embed(ctx, appID)
            


async def _random_game(ctx:tanjun.abc.Context) -> None:

    gdata = (requests.get("https://api.steampowered.com/IStoreService/GetAppList/v1/?&include_games=true&include_dlc=false&key={}".format(STEAM_KEY))).json()
    apps = gdata["response"]["apps"]

    choice = random.choice(apps)

    appid = choice["appid"]

    gddata = (requests.get(
        "https://store.steampowered.com/api/appdetails/?appids={}&l=english".format(appid))).json()

    appdetails = gddata.get("{}".format(appid)).get("data")

    categories = appdetails.get("categories")
    genres = appdetails.get("genres")

    return categories, genres, appid


async def _game_embed(ctx:tanjun.abc.Context, appID) -> None:
    
    # API request to then get game details using appID.
    gsdata = (requests.get(
        "https://store.steampowered.com/api/appdetails/?appids={}&l=english".format(appID))).json()

    # Remove html content from description and notice.
    cleanr = re.compile('<.*?>')

    def cleanhtml(raw_html):
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    # API request to get reviews for games.

    rdata = (requests.get("https://store.steampowered.com/appreviews/{}?json=1".format(appID))).json()

    # Accessing data dictionary and assigned them values.

    appdetails = gsdata.get("{}".format(appID)).get("data")
    description = appdetails.get("short_description")

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
        notice = appdetails["legal_notice"]
        snotice = sent_tokenize(notice)
        notice = " ".join([str(item) for item in snotice[:1]])
        embed.set_footer(text=cleanhtml(notice))

    # Adding multiple devs to developer field.

    dev = ", ".join([str(item)
                     for item in appdetails.get("developers")])
    embed.add_field(name="Developers: ",
                    value=dev, inline=True)

    # Price checks for games.

    price = appdetails.get("price_overview")

    if appdetails["is_free"] == True:
        embed.add_field(name="Price: ", value="Free", inline=True)

    elif appdetails["release_date"]["coming_soon"] == True and price is None:
        embed.add_field(name="Price: ", value="Coming Soon.", inline=True)

    elif price.get("initial_formatted") != "":
        embed.add_field(name="Price: ", value="~~{}~~".format(
            price.get("initial_formatted")) + " " + "**{}**".format(price.get("final_formatted")), inline=True)

    else:
        embed.add_field(
            name="Price: ", value=price["final_formatted"], inline=True)

    review = rdata["query_summary"]["review_score_desc"]

    embed.add_field(name="Review:", value = review, inline = True)

    await ctx.edit_last_response(content="", embed=embed)



@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
