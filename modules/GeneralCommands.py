import tanjun
import hikari
import random

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("d20", "Roll a d20 dice.")
async def roll_d20(ctx: tanjun.abc.SlashContext) -> None:

    roll = random.randint(1, 20)

    await ctx.respond(ctx.author + " rolled a " + roll + "!", delete_after=60)
    

@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
