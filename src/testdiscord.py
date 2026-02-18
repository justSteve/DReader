import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", description=description, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.close()


token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise ValueError("DISCORD_TOKEN environment variable not set")
bot.run(token)
