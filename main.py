import json
import os
from itertools import cycle

import discord
import motor.motor_asyncio
import requests
from discord.ext import commands, tasks

with open("token.json") as json_file:
    data = json.load(json_file)

mongo_connect = data["mongoconnect"]
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_connect)

levelling = cluster["rekky"]["levelling"]
prefix_collection = cluster["rekky"]["prefix"]
message_collection = cluster["rekky"]["messageLog"]

intents = discord.Intents(messages=True, guilds=True, members=True)
client = commands.Bot(command_prefix=".", intents=intents, help_command=None)


@client.event
async def on_message(message):
    await message_collection.insert_one(
        {"userID": message.author.id, "message": message.content}
    )
    await client.process_commands(message)


@client.event
async def on_ready():
    print("Bot online")


client.cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_connect)

client.levelling = client.cluster["rekky"]["levelling"]
client.prefixCollection = client.cluster["rekky"]["prefix"]
client.memeCollection = client.cluster["rekky"]["memes"]


@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{next(status)}"
        )
    )


@change_status.before_loop
async def before_change_status():
    await client.wait_until_ready()
    global status
    status = cycle(
        [
            "Message me to invite me!",
            f"over {len(client.guilds)} guilds",
            f"over {len(client.users)} users",
        ]
    )


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

discord_bot_list_auth = data["discord_bot_list_auth"]
true = data["true"]


@tasks.loop(seconds=520)
async def publish_stats():
    await client.wait_until_ready()
    discord_botlist_url = "https://discordbotlist.com/api/v1/bots/applications/stats"
    discord_botlist_body = {"guilds": len(client.guilds), "users": len(client.users)}
    discord_botlist_headers = {"Authorization": discord_bot_list_auth}
    request_discord_botlist = requests.post(
        discord_botlist_url, data=discord_botlist_body, headers=discord_botlist_headers
    )
    print(f"discord bot list post - {request_discord_botlist}")


publish_stats.start()

change_status.start()

token = data["token"]
client.run(token)
