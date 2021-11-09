from asyncio.events import get_running_loop
import requests
import difflib
import asyncio


def main(game):

    gres = requests.get(
        "https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    gdata = gres.json()

    apps = gdata["applist"]["apps"]

    glist = [x["name"].lower() for x in apps if x["name"]]

    possibilities = glist

    matches = difflib.get_close_matches(
        game.lower(), possibilities, n=1, cutoff=0.3)

    app = [x for x in apps if matches[0] == x["name"].lower()]

    appID = str(app[0]["appid"])
    name = app[0]["name"]

    return appID, name


async def SteamSearch(game):
    loop = asyncio.get_running_loop()

    results = await loop.run_in_executor(None, main, (game))

    return results
