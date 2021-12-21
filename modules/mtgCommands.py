from hikari.embeds import Embed
import tanjun
import hikari
import requests

component = tanjun.Component()

@component.with_slash_command
@tanjun.with_str_slash_option("card", "Card to pull up.")
@tanjun.as_slash_command("mtg-card", "Look up a certain card.")
async def mtg_card(ctx:tanjun.abc.SlashContext, card:str):

    try:

        mtgdata = (requests.get("https://api.magicthegathering.io/v1/cards?name={}&pageSize=1&contains=imageUrl".format(card.lower()))).json()

        card = mtgdata.get("cards")[0]

        await ctx.respond(card["imageUrl"])
    
    except IndexError:
        await ctx.respond("Please double check the spelling of the card.")


@component.with_slash_command
@tanjun.with_str_slash_option("card", "Card to pull up.")
@tanjun.as_slash_command("mtg-rulings", "Look up cards ruling.")
async def mtg_rulings(ctx:tanjun.abc.SlashContext, card:str):


    try:
        mtgdata = (requests.get("https://api.magicthegathering.io/v1/cards?name={}&pageSize=1&contains=imageUrl".format(card.lower()))).json()

        card = mtgdata.get("cards")[0]

        rulings = card["rulings"]        

        embed = hikari.Embed(
            title = "Rulings.",
            color = hikari.Color(0xFF0000)
        )

        embed.set_thumbnail(card["imageUrl"])

        for x in rulings:
            embed.add_field(name="Date: {}".format(x["date"]), value= x["text"], inline=False)

        await ctx.respond(embed)
    
    except IndexError:
        await ctx.respond("Please double check the spelling of the card.")

    except KeyError:
        await ctx.respond("This card does not have any rulings.")


@component.with_slash_command
@tanjun.with_str_slash_option("card", "Card with similar names to pull up.")
@tanjun.as_slash_command("mtg-list", "Look up a list of cards.")
async def mtg_list(ctx:tanjun.abc.SlashContext, card:str):

    try:

        mtgdata = (requests.get("https://api.magicthegathering.io/v1/cards?name={}&pageSize=7&contains=imageUrl".format(card.lower()))).json()

        cards = mtgdata.get("cards")
            

        embed = hikari.Embed(
            title = "Cards",
            color = hikari.Color(0x228b22)
        )


        for x in cards:
            embed.add_field(name=x["name"], value="Set: " + x["setName"], inline=False)

        await ctx.respond(embed)
    except IndexError:
        await ctx.respond("Please double check the spelling of the card.")


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())