import requests
import difflib


def SteamSearch(game):

    gres = requests.get(
        "https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    gdata = gres.json()

    apps = gdata["applist"]["apps"]

    glist = [x["name"].lower() for x in apps if x["name"]]

    possibilities = glist

    matches = difflib.get_close_matches(
        game.lower(), possibilities, n=1, cutoff=0.3)

    for x in gdata["applist"]["apps"]:
        if (matches[0] == x["name"].lower()):
            appID = (x["appid"])

    return appID
