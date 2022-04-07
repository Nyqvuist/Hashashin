from datetime import datetime, date, time
from hikari.embeds import Embed
import tanjun
import hikari
import requests
from datetime import timedelta

elden_group = tanjun.slash_command_group("eldenring", "Elden Ring commands.")

@elden_group.with_command
@tanjun.with_str_slash_option("name", "The name of the NPC")
@tanjun.as_slash_command("npc", "Search for a NPC")
async def npc_search(ctx: tanjun.abc.SlashContext, name: str) -> None:

    ndata = (requests.get("https://eldenring.fanapis.com/api/npcs?name={}".format(name))).json()


    if ndata["success"] == True:
        ndata = ndata["data"][0]

        embed = hikari.Embed(
            title=ndata["name"],
            description=ndata["quote"],
            color=hikari.Color(0x333049)
        )
        
        embed.set_image(ndata["image"])

        embed.add_field(name="Location: ", value=ndata["location"], inline=True)
        embed.add_field(name="Role: ", value=ndata["role"], inline=True)

        await ctx.respond(embed)
    else:
        await ctx.respond("Please double check the name of the NPC.")

    
    

@elden_group.with_command
@tanjun.with_str_slash_option("name", "The name of the weapon.")
@tanjun.as_slash_command("weapon", "Search for a weapon.")
async def weapon_search(ctx: tanjun.abc.SlashContext, name: str) -> None:
    
    wdata = (requests.get("https://eldenring.fanapis.com/api/weapons?name={}".format(name))).json()

    if wdata["success"] == True:
        wdata = wdata["data"][0]

        print(wdata)







































component = tanjun.Component().add_slash_command(elden_group)

@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())