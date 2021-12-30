import tanjun
import hikari
from lib import lib
import os
from dotenv import load_dotenv
import requests

load_dotenv()

HALO_TOKEN = os.getenv("HALO_TOKEN")

lib = lib(token=HALO_TOKEN)

component = tanjun.Component()

@component.with_slash_command
@tanjun.with_str_slash_option("ign", "User's IGN.")
@tanjun.as_slash_command("halo-rank", "Look up user's current halo rank.")
async def halo_rank(ctx:tanjun.abc.SlashContext, ign:str):
    pass



@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())