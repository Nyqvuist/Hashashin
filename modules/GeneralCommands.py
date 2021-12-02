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

        await ctx.respond("**" + ctx.member.display_name + "**" + " rolled a " + str(roll) + "!", delete_after=60)

    elif d6:

        roll = random.randint(1, 6)

        await ctx.respond("**" + ctx.member.display_name + "**" + " rolled a " + str(roll) + "!", delete_after=60)
    
    elif coin:

        coinflip = ['Heads','Tails']

        roll = random.choice(coinflip)

        await ctx.respond("**" + ctx.member.display_name + "**" + " flipped " + str(roll) + "!", delete_after=60)
    
    else:

        await ctx.respond("Please choose a dice or coin!", delete_after=30)


    

@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
