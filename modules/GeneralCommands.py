import tanjun
import hikari
import random
import typing
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import bot
from datetime import date, datetime



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

@component.with_slash_command
@tanjun.with_str_slash_option("name", "please name the job.")
@tanjun.with_mentionable_slash_option("mentionable", "option to mention a role", default=None)
@tanjun.with_channel_slash_option("channel", "channel to send the message to.")
@tanjun.with_int_slash_option("minute", "minute needs to be in military time.")
@tanjun.with_int_slash_option("hour", "hour needs to be in military time.")
@tanjun.with_str_slash_option("message", "message to schedule daily.")
@tanjun.as_slash_command("sched-daily", "schedule a daily message.")
async def sched_daily(ctx: tanjun.abc.SlashContext, message: str, hour: int, minute: int, channel: hikari.InteractionChannel, name:str, mentionable: hikari.Role) -> None:
    
    if mentionable:
        async def daily():
            await ctx.rest.create_message(
                channel=channel,
                content=message,
                role_mentions=(mentionable, True)
            )
        bot.scheduler.add_job(daily, 'cron', hour=hour, minute=minute, id=name)
    else:
        async def daily():
            await ctx.rest.create_message(
                channel=channel,
                content=message,
            )
        bot.scheduler.add_job(daily, 'cron', hour=hour, minute=minute, id=name)
    
    await ctx.respond("Your job " + "`" + name + "`" + " has been added.")


@component.with_slash_command
@tanjun.with_str_slash_option("name", "name of the job to delete.")
@tanjun.as_slash_command("sched-delete", "delete a scheduled job.")
async def sched_delete(ctx: tanjun.abc.SlashContext, name:str) -> None:
    try:
        bot.scheduler.remove_job(name)
    except:
        pass
    await ctx.respond("You deleted the " + "`" + name + "`" + " job.")

@component.with_slash_command
@tanjun.with_str_slash_option("name", "please name the job.")
@tanjun.with_mentionable_slash_option("mentionable", "option to mention a role", default=None)
@tanjun.with_channel_slash_option("channel", "channel to send the message to.")
@tanjun.with_int_slash_option("minute", "minute needs to be in military time.")
@tanjun.with_int_slash_option("hour", "hour needs to be in military time.")
@tanjun.with_str_slash_option("day", "which day to schedule job.")
@tanjun.with_str_slash_option("message", "message to schedule daily.")
@tanjun.as_slash_command("sched-weekly", "schedule a weekly message.")
async def sched_weekly(ctx: tanjun.abc.SlashContext, message: str, hour: int, minute: int, channel: hikari.InteractionChannel, name:str, mentionable: hikari.Role, day:str) -> None:
    
    convert = {
        'monday':0,
        'tuesday':1,
        "wednesday":2,
        'thursday':3,
        'friday':4,
        'saturday':5,
        'sunday':6
    }

    day = convert[day.lower()]

    if mentionable:
        async def weekly():
            await ctx.rest.create_message(
                channel=channel,
                content=message,
                role_mentions=(mentionable, True)
            )
        bot.scheduler.add_job(weekly, 'cron', day_of_week=day, hour=hour, minute=minute, id=name)
    else:
        async def weekly():
            await ctx.rest.create_message(
                channel=channel,
                content=message,
            )
        bot.scheduler.add_job(weekly, 'cron', day_of_week=day, hour=hour, minute=minute, id=name)
    
    await ctx.respond("Your job " + "`" + name + "`" + " has been added.")


@component.with_slash_command
@tanjun.with_str_slash_option("name", "please name the job.")
@tanjun.with_mentionable_slash_option("mentionable", "option to mention a role", default=None)
@tanjun.with_channel_slash_option("channel", "channel to send the message to.")
@tanjun.with_str_slash_option("date", "yyyy-mm-dd hh:mm:ss")
@tanjun.with_str_slash_option("message", "message to schedule once.")
@tanjun.as_slash_command("sched-once", "schedule a message once.")
async def sched_once(ctx: tanjun.abc.SlashContext, message: str, date:str, channel: hikari.InteractionChannel, name:str, mentionable: hikari.Role) -> None:
    
    if mentionable:
        async def once():
            await ctx.rest.create_message(
                channel=channel,
                content=message,
                role_mentions=(mentionable, True)
            )
        bot.scheduler.add_job(once, 'date', run_date=str(date), id=name)
    else:
        async def once():
            await ctx.rest.create_message(
                channel=channel,
                content=message,
            )
        print(str(date))
        bot.scheduler.add_job(once,'date', run_date=str(date), id=name)
        
    
    await ctx.respond("Your job " + "`" + name + "`" + " has been added.")

@component.with_slash_command
@tanjun.as_slash_command("sched-jobs", "check a list of jobs.")
async def sched_jobs(ctx:tanjun.abc.SlashContext) -> None:

   jobs = bot.scheduler.get_jobs()

   if jobs == []:
       await ctx.respond("There are no current jobs right now.")
   else:
        await ctx.respond(jobs)

@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
