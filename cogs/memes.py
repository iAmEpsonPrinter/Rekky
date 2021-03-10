import random

from discord.ext import commands


class Memes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        lol = []
        async for x in self.client.memeCollection.find({"subreddit": "$all"}):
            lol.append(x)
            print(x)

        print(lol)

        statss = []
        async for stat in self.client.memeCollection.find(
            {"subreddit": random.choice(self.client.subredditList)}
        ):
            statss.append(stat)

        print(random.choice([stat["url"] for stat in statss]))

        await ctx.send(f'{random.choice([stat["url"] for stat in statss])}')
        await ctx.send(f'{random.choice([stat["url"] for stat in statss])}')
        await ctx.send(f'{random.choice([stat["url"] for stat in statss])}')


def setup(client):
    client.add_cog(Memes(client))
