import discord
from discord.ext import commands


class Helpp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        stats_commands = {
            ".announce": "`[ChannelMention] [announcement]`",
            ".prefix": "`[NewPrefix]`",
            ".purge": "`[amount]`",
            ".meme": "`Sends random memes from a huge database!`",
        }

        misc_commands = {
            ".help": "`Lists all of the commands for the bot.`",
            ".vote": "`Messages the user voting information`",
            ".ping": "`Displays the bots ping`",
        }
        embed = discord.Embed(title="Commands", color=discord.colour.Color.green())

        for command_name in stats_commands:
            command_description = stats_commands[command_name]
            embed.add_field(name=command_name, value=command_description, inline=True)

        for command_name in misc_commands:
            command_description = misc_commands[command_name]
            embed.add_field(name=command_name, value=command_description, inline=True)

        embed.set_author(name="Discord Pandemic", icon_url=self.client.user.avatar_url)
        embed.set_footer(
            text="Like the bot? Consider voting for it by typing "
            ".vote (It would really help us out!)",
            icon_url=self.client.user.avatar_url,
        )
        embed.set_author(name="Discord Pandemic", icon_url=self.client.user.avatar_url)
        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Helpp(client))
