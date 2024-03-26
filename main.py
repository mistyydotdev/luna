from discord import ApplicationContext, Intents
import os
from client import LunaClient
from models.base import Base
from models.user import User
import json

intents = Intents()
intents.members = True
intents.guilds = True

client = LunaClient(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user.name} has logged in.")


@client.slash_command(guild_ids=[957867801119449109])
async def hello(ctx: ApplicationContext):
    await ctx.respond(f"Hello {ctx.author.name}")


for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")
        print(f"Loaded cog.{cog[:-3]}")
    else:
        continue


Base.metadata.create_all(bind=client.engine)

settings = None

with open("settings.json") as f:
    settings = json.load(f)

client.run(settings["token"])