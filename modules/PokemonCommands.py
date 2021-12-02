from hikari.embeds import Embed
import tanjun
import hikari
import requests

component = tanjun.Component()

@component.with_slash_command
@tanjun.with_str_slash_option("nature", "Nature of pokemon.")
@tanjun.as_slash_command("pokemon-nature", "Get nature information of a pokemon.")
async def pokemon_nature(ctx:tanjun.abc.SlashContext, nature:str):
    
    pokemondata = (requests.get("https://pokeapi.co/api/v2/nature/{}/".format(nature.lower()))).json()
    move_preference = pokemondata['move_battle_style_preferences']

    embed= hikari.Embed(
        title = pokemondata["name"].title(),
        color = hikari.Color(0xffcb05)
    )

    embed.add_field(name="Decreased Stat", value = pokemondata['decreased_stat']['name'].title(), inline=True)
    embed.add_field(name="Increased Stat", value = pokemondata['increased_stat']['name'].title(), inline=True)
    embed.add_field(name="Likes Flavor", value = pokemondata['likes_flavor']['name'].title(), inline=True)
    embed.add_field(name="Hates Flavor", value = pokemondata['hates_flavor']['name'].title(), inline=True)

    for x in move_preference:
        embed.add_field(name=x['move_battle_style']['name'].title(), value = "High HP Preference: " + str(x['high_hp_preference']) + "%" + "\nLow HP Preference: " + str(x['low_hp_preference']) + "%", inline=False)

    await ctx.respond(embed)



@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())