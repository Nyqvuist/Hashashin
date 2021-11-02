import steam
from steam.webapi import WebAPI
import os
import requests
import difflib


def SteamSearch(game):

    STEAM_KEY = os.getenv("STEAM_KEY")

    api = WebAPI(key=STEAM_KEY)

    gres = requests.get(
        "https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    gdata = gres.json()

    list = []

    for x in gdata["applist"]["apps"]:
        if x["name"]:
            list.append(x["name"].lower())

    possibilities = list

    matches = difflib.get_close_matches(
        game.lower(), possibilities, n=1, cutoff=0.3)

    for x in gdata["applist"]["apps"]:
        if (matches[0] == x["name"].lower()):
            appID = (x["appid"])

    return appID
