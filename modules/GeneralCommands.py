import tanjun
import hikari
import random
import typing
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import main
from datetime import date, datetime
import difflib



dice_group = tanjun.slash_command_group("roll", "Roll a dice/coin.")
component = tanjun.Component().add_slash_command(dice_group)


@dice_group.with_command
@tanjun.as_slash_command("d20", "Roll a d20")
async def roll_d20(ctx: tanjun.abc.SlashContext) -> None:
    roll = random.randint(1, 20)

    await ctx.respond("**" + ctx.member.display_name + "**" + " rolled a " + str(roll) + "!")

@dice_group.with_command
@tanjun.as_slash_command("d6", "Roll a d6")
async def roll_d6(ctx: tanjun.abc.SlashContext) -> None:
    roll = random.randint(1, 6)

    await ctx.respond("**" + ctx.member.display_name + "**" + " rolled a " + str(roll) + "!")

@dice_group.with_command
@tanjun.as_slash_command("coin", "Flip a coin")
async def flip_coin(ctx: tanjun.abc.SlashContext) -> None:
    coinflip = ['Heads','Tails']

    roll = random.choice(coinflip)

    await ctx.respond("**" + ctx.member.display_name + "**" + " flipped " + str(roll) + "!")

@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
