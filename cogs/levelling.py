from discord.ext import commands


class Levelling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        stats = await self.client.levelling.find_one({"id": message.author.id})
        if stats:  # on message check to see if message author is in database
            xp = stats["xp"] + 1  # add one to xp
            self.client.levelling.update_one(
                {"id": message.author.id}, {"$set": {"xp": xp}}
            )
            level = stats["level"]

            if xp >= 5 * (level ** 2) + 50 * level + 100:
                level += 1
                print(level)
                self.client.levelling.update_one(
                    {"id": message.author.id}, {"$set": {"level": level}}
                )
                await message.channel.send(
                    f"Well done {message.author.mention}! "
                    f"You have leveled up to **level: {level}**!"
                )

        elif (
            stats is None
        ):  # if author is not in database add them to database and give them 100 xp
            self.client.levelling.insert_one(
                {"id": message.author.id, "xp": 0, "level": 0}
            )

        # if author is not in database add them to database and give them 100 xp


def setup(client):
    client.add_cog(Levelling(client))
