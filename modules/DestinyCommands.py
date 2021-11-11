import tanjun
import hikari
from nltk.tokenize import sent_tokenize
import datetime
import difflib
import re
import os
import requests
import nltk
import asyncio

API_KEY = os.environ.get("DESTINY_KEY")


component = tanjun.Component()


@component.with_slash_command
@tanjun.with_str_slash_option("id", "The name of the destiny profile.")
@tanjun.as_slash_command("dsearch", "Search for a bungie name.")
async def id_search(ctx: tanjun.abc.Context, id: str) -> None:
    pass


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
