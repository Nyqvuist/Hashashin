import hikari
import tanjun
import os
import logging
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 680660671918243842

logging.basicConfig(level=logging.INFO)

bot = hikari.GatewayBot(DISCORD_TOKEN)

client = tanjun.Client.from_gateway_bot(
    bot, declare_global_commands=True, mention_prefix=True)


@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    print("Hashashin is online!")


for filename in os.listdir("./modules"):
    if filename.endswith('.py'):
        client.load_modules(f"modules.{filename[:-3]}")

bot.run()
