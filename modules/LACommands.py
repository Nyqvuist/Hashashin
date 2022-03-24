from datetime import datetime, date, time
from hikari.embeds import Embed
import tanjun
import hikari
import requests
from datetime import timedelta

component = tanjun.Component()

events = {
    "Thursday": ["Chaos Gate", "Ghost Ship"],
    "Friday": ["World Boss"],
    "Saturday": ["Ghost Ship", "Chaos Gate"],
    "Sunday": ["Field Boss", "Chaos Gate"],
    "Monday": ["Chaos Gate"],
    "Tuesday": ["Ghost Ship", "World Boss"],
    "Wednesday": ["There Are No Events Today"]
}


@component.with_slash_command
@tanjun.as_slash_command("event", "Todays Lost Ark Events.")
async def event(ctx: tanjun.abc.SlashContext) -> None:
    now = datetime.now()
    date = now.strftime("%A")
    time = now.strftime("%H:%M:%S")
    delta = timedelta(hours=1)
    next_hour = (now + delta).replace(microsecond=0, second=0, minute=0)
    wait_minutes = (next_hour - now).seconds
    wait_minutes = wait_minutes / 60

    embed = hikari.Embed(
        title="Today's Events"
    )

    
    for event in events:
        if date == event:
            for x in events[event]:
                if x == "There Are No Events Today":
                    embed.add_field(name="There Are No Events Today.", value="\u200b", inline=True)
                else:
                    embed.add_field(name=x, value="in " + str(int(wait_minutes) + 1) + " minutes.", inline=False)
                    
    await ctx.respond(embed)




@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())