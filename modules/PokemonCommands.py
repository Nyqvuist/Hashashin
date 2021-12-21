from hikari.embeds import Embed
from hikari.internal.data_binding import JSONDecodeError
import tanjun
import hikari
import requests
import difflib

component = tanjun.Component()

@component.with_slash_command
@tanjun.with_str_slash_option("nature", "Nature of pokemon.")
@tanjun.as_slash_command("pokemon-nature", "Get nature information of a pokemon.")
async def pokemon_nature(ctx:tanjun.abc.SlashContext, nature:str):
    
    possibilities = ["adamant","bashful","bold","brave","calm","careful","docile","gentle","hardy","hasty","impish","jolly","lax","lonely","mild","modest","naive","naughty","quiet","quirky","rash","relaxed","sassy","serious","timid"]
    
    matches = difflib.get_close_matches(
        nature.lower(), possibilities, n=1, cutoff=0.3)
    
    pokemondata = (requests.get("https://pokeapi.co/api/v2/nature/{}/".format(matches[0].lower()))).json()
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


@component.with_slash_command
@tanjun.with_str_slash_option("version", "The game version.")
@tanjun.with_str_slash_option("pokemon", "The specified pokemon.")
@tanjun.as_slash_command("pokemon-route", "Get location of specific pokemon.")
async def pokemon_route(ctx:tanjun.abc.SlashContext, pokemon:str, version:str):

    try:
        possibilities = ["red","blue","diamond","pearl","platinum","yellow","gold","silver","crystal","firered","leafgreen","heartgold","soulsilver","ruby","sapphire","emerald","x","y","omega-ruby","alpha-sapphire","black","white"]

        matches = difflib.get_close_matches(
            version.lower(), possibilities, n=1, cutoff=0.3)

        pokemondata = (requests.get("https://pokeapi.co/api/v2/pokemon/{}/encounters".format(pokemon.lower()))).json()

        vlist = []
        dlist = []
        

        for x in pokemondata:
            version = x["version_details"][0]
            if version["version"]["name"] == matches[0]:
                vlist.append(x)
            else:
                if version["version"]["name"]:
                    dlist.append(version["version"]["name"])
                    dlist = list(set(dlist))

        if len(vlist) > 0:
            embed = hikari.Embed(
                title = pokemon.title() + " Routes " "- Version: " + matches[0].title(),
                color = hikari.Color(0xee1515)
                )

            for y in vlist:
                version = y["version_details"][0]
                name = y["location_area"]["name"].replace("-", " ")
                embed.add_field(name=name.title(), value="Encounter Potential: " + str(version["max_chance"]) + "%", inline=False)

            await ctx.respond(embed)
            
        elif len(vlist) <= 1 and dlist == []:
            await ctx.respond("This pokemon cannot be found in wild grass.")
            
        elif vlist == [] and len(dlist) > 0:
            embed = hikari.Embed(
                title = pokemon.title() + " can be found in these versions!",
                color = hikari.Color(0xee1515)
                )
            for x in dlist:
                embed.add_field(name=x.title(), value="\u200b", inline=True)

            await ctx.respond(embed)   
            
    except JSONDecodeError:
        await ctx.respond("Make sure the pokemon's name is typed correctly!")


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())