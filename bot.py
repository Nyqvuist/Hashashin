import hikari
import tanjun
import os
import logging
from dotenv import load_dotenv
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

LAVALINK_HOST = os.getenv("LAVALINK_HOST")
LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD")
LAVALINK_PORT = os.getenv("LAVALINK_PORT")

logging.basicConfig(level=logging.INFO)

bot = hikari.GatewayBot(DISCORD_TOKEN)

client = tanjun.Client.from_gateway_bot(
    bot, declare_global_commands=True, mention_prefix=True)


@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    print("Hashashin is online!")


async def tick():
    await client.rest.create_message(
        channel=767527790802632714,
        content="test message to message @The Three Time",
        role_mentions=True
    )

async def sched_start():
    loop = asyncio.get_running_loop()

    results = await loop.run_in_executor(None, scheduler.start)

    return results


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'cron', day_of_week='6',hour='12', minute='30')
    scheduler.start()

for filename in os.listdir("./modules"):
    if filename.endswith('.py'):
        client.load_modules(f"modules.{filename[:-3]}")

bot.run()

