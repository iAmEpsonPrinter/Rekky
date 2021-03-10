import discord
from discord.ext import commands


class Errorhandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=str(self.client.user), color=0xFF0000)
            embed.add_field(
                name=f"Invalid parameters for {ctx.command.name} command",
                value=f"{error}",
                inline=False,
            )
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=str(self.client.user), color=0xFF0000)
            embed.add_field(
                name=f"Unknown parameter for {ctx.command.name} command",
                value=f"{error}",
                inline=False,
            )
            await ctx.send(embed=embed)
        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title=str(self.client.user), color=0xFF0000)
            embed.add_field(
                name=f" Bot missing permissions for {ctx.command.name} command",
                value=f"{error}",
                inline=False,
            )
            await ctx.send(embed=embed)
        print(error)


def setup(client):
    client.add_cog(Errorhandling(client))
