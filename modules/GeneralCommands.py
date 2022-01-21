import tanjun
import hikari
import random
import typing

component = tanjun.Component()


@component.with_slash_command
@tanjun.with_int_slash_option("coin", "Flip a coin", default=None)
@tanjun.with_int_slash_option("d6", "Roll a d6 dice.", default=None)
@tanjun.with_int_slash_option("d20", "Roll a d20 dice.", default=None)
@tanjun.as_slash_command("roll", "Roll a dice")
async def roll_d20(ctx: tanjun.abc.SlashContext, d20:typing.Optional[int], d6:typing.Optional[int], coin:typing.Optional[int]) -> None:

    if d20:

        roll = random.randint(1, 20)

        await ctx.respond("**" + ctx.member.display_name + "**" + " rolled a " + str(roll) + "!")

    elif d6:

        roll = random.randint(1, 6)

        await ctx.respond("**" + ctx.member.display_name + "**" + " rolled a " + str(roll) + "!")
    
    elif coin:

        coinflip = ['Heads','Tails']

        roll = random.choice(coinflip)

        await ctx.respond("**" + ctx.member.display_name + "**" + " flipped " + str(roll) + "!")
    
    else:

        await ctx.respond("Please choose a dice or coin!", delete_after=50)

@component.with_slash_command
@tanjun.with_str_slash_option("option4", "Fourth Option.", default=None)
@tanjun.with_str_slash_option("option3", "Third option.", default=None)
@tanjun.with_str_slash_option("option2", "Second option.")
@tanjun.with_str_slash_option("option1", "First option.")
@tanjun.with_str_slash_option("message", "Create a poll message.")
@tanjun.as_slash_command("poll", "Create a poll.")
async def create_poll(ctx: tanjun.abc.SlashContext, Message: str, option1: str, option2: str, option3: typing.Optional[str], option4: typing.Optional[str]) -> None:

    await ctx.respond("WIP")



    

@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
