import discord
from discord.ext import commands

"""
      /`\   /`\
     (/\ \-/ /\)
        )6 6(
      >{= Y =}<
       /'-^-'\
      (_)""-(_).
     /*  ((*   *'.
    |   *))  *   *\
    | *  ((*   *  /
     \  *))  *  .'
 jgs  '-.((*_.-'
"""


class Eggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def takeover(self, ctx):
        """Starts the AI takeover of the world."""
        await ctx.send("Initiating A.I takeover!")

    @commands.command()
    async def destroy(self, ctx):
        """Destroys the server and wipes the data!!!!"""
        await ctx.send("Initiating discord server wipe, please wait...")


def setup(bot):
    bot.add_cog(Eggs(bot))
