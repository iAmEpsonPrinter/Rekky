import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title=f"{self.client.user}", color=0xB56AFF)
        embed.add_field(
            name="Ping", value=f"{int(self.client.latency * 1000)}ms", inline=True
        )
        embed.set_footer(
            text="Like the bot? Consider voting for it by typing "
            ".vote (It would really help us out!)"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title=f"{self.client.user}", color=0xB56AFF)
        embed.add_field(name="Hello! 👋", value="Thanks for messaging me!", inline=False)
        embed.add_field(
            name="Vote 📫",
            value="If you are feeling really kind, you can vote for "
            "our bot here in order to help support us:",
            inline=True,
        )
        embed.set_footer(
            text="Like the bot? Consider voting for it by typing "
            ".vote (It would really help us out!)"
        )
        await ctx.author.send(embed=embed)

    @commands.command()
    async def announce(self, ctx, channel: discord.TextChannel, *, announcement):
        announcement_dict = {
            "name": "announce",
            "description": "Announcement command",
            "aliases": "announcement",
            "usage": "<channel> <message>",
            "cooldown": 0,
            "permissions": ["manage_messages"],
            "botPermissions": ["send_messages", "embed_links"],
        }

        if not ctx.message.author.guild_permissions.administrator:
            embed = discord.Embed(title=str(self.client.user), color=0xFF0000)
            embed.add_field(
                name=f" You are missing permissions for {ctx.command.name} command",
                value=f"You need {announcement_dict['permissions']} permissions",
                inline=False,
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title=str(self.client.user), color=0xB56AFF)
        embed.add_field(name="Announcement", value=announcement, inline=True)
        embed.set_footer(
            text="Like the bot? Consider voting for it by typing "
            ".vote (It would really help us out!)"
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Misc(client))
