import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def purge(self, ctx, amount: int):
        purge_dict = {
            "name": "announce",
            "description": "Announcement command",
            "aliases": "announcement",
            "usage": "<channel> <message>",
            "cooldown": 0,
            "permissions": ["manage_messages"],
            "botPermissions": ["send_messages", "embed_links"],
        }
        if not ctx.message.author.guild_permissions.manage_messages:
            embed = discord.Embed(title=str(self.client.user), color=0xFF0000)
            embed.add_field(
                name=f"You are missing permissions for **{ctx.command.name}** command",
                value=f"You need **{purge_dict['permissions']}** permissions",
                inline=False,
            )
            embed.set_footer(
                text="Like the bot? Consider voting for it by typing "
                ".vote (It would really help us out!)"
            )
            await ctx.send(embed=embed)
            return
        await ctx.channel.purge(limit=amount)
        if amount > 100:
            await ctx.send(
                f"Deleted {100}/{amount} messages! I can only delete 100 messages at a time!",
                delete_after=5,
            )
        else:
            embed = discord.Embed(
                title=str(self.client.user), color=discord.colour.Color.green()
            )
            embed.add_field(
                name="Successfully executed purge",
                value=f"Successfully deleted **{amount}/{amount}** messages!",
                inline=False,
            )
            embed.set_footer(
                text="Like the bot? Consider voting for it by typing "
                ".vote (It would really help us out!)"
            )
            await ctx.send(embed=embed, delete_after=5)


def setup(client):
    client.add_cog(Moderation(client))
