import discord
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(client):
    bot.add_cog(Test(bot))

