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
    client.status = cycle(
        [
            "Message me to invite me!",
            f" {len(client.guilds)} guilds",
            f" {len(client.users)} users",
        ]
    )
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{next(client.status)}"
        )
    )


@change_status.before_loop
async def before_change_status():
    await client.wait_until_ready()
    print(f"Guilds - {len(client.guilds)}")
    print(f"Users - {len(client.users)}")
    client.status = cycle(
        [
            "Message me to invite me!",
            f" {len(client.guilds)} guilds",
            f" {len(client.users)} users",
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




@client.event
async def on_guild_join(guild):
    async for entry in guild.audit_logs(action=discord.AuditLogAction.bot_add):
        try:
            if entry.target == client.user:
                embed = discord.Embed(
                    title="Hello! 👋", color=discord.colour.Color.green()
                )
                embed.set_author(
                    name="Discord Pandemic", icon_url=client.user.avatar_url
                )
                embed.add_field(
                    name="Thank you for inviting me! 😊",
                    value="Currently this bot does not have all of "
                    "the advertised features, as stated in the "
                    "bot description. However, by inviting the "
                    "bot you are allowing us to test new features "
                    "(such as statistics) and much more behind the scenes.",
                    inline=False,
                )
                embed.add_field(
                    name="Support 🆘",
                    value="For the latest changelog and support "
                    "please join: https://discord.gg/xDaUF2UaQZ",
                    inline=False,
                )
                embed.set_footer(
                    text="Like the bot? Consider voting for it by typing "
                    ".vote (It would really help us out!)"
                )
                await entry.user.send(embed=embed)
        except PermissionError:
            print("Permission Error")
    channel = await client.fetch_channel(812017926005719062)
    embed = discord.Embed(
        title=client.user.display_name, color=discord.colour.Color.green()
    )
    embed.set_author(name=client.user.display_name, icon_url=client.user.avatar_url)
    embed.add_field(name=f"New server - {guild.name}", value=guild.name, inline=True)
    embed.add_field(
        name="New user count",
        value=f"{len(client.users)} (+{guild.member_count})",
        inline=True,
    )
    embed.add_field(
        name="New Guild Count", value=f"{len(client.guilds)} (+1)", inline=True
    )
    embed.add_field(
        name="New Emoji Count",
        value=f"{len(client.emojis)} (+{len(guild.emojis)})",
        inline=True,
    )
    embed.set_footer(
        text="Like the bot? Consider voting for it by typing .vote (It would really help us out!)"
    )
    await channel.send(embed=embed)


@client.event
async def on_guild_remove(guild):
    channel = await client.fetch_channel(812017947659730965)
    embed = discord.Embed(
        title=client.user.display_name, color=discord.colour.Color.red()
    )
    embed.set_author(name=client.user.display_name, icon_url=client.user.avatar_url)
    embed.add_field(name=f"New server - {guild.name}", value=guild.name, inline=True)
    embed.add_field(
        name="New user count",
        value=f"{len(client.users)} (-{guild.member_count})",
        inline=True,
    )
    embed.add_field(
        name="New Guild Count", value=f"{len(client.guilds)} (-1)", inline=True
    )
    embed.add_field(
        name="New Emoji Count",
        value=f"{len(client.emojis)} (-{len(guild.emojis)})",
        inline=True,
    )
    embed.set_footer(
        text="Like the bot? Consider voting for it by typing .vote (It would really help us out!)"
    )
    await channel.send(embed=embed)



publish_stats.start()
change_status.start()

token = data["token"]
client.run(token)
