import logging

import statcord
from discord.ext import commands

logging.basicConfig(format="%(asctime)s -  %(levelname)s -  %(message)s")
logger = logging.getLogger("statcord")
logger.setLevel(logging.INFO)


class StatcordPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = "statcord.com-atixikZ8cflZdQO2kOEi"
        self.api = statcord.Client(self.bot, self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.api.command_run(ctx)


def setup(bot):
    bot.add_cog(StatcordPost(bot))
