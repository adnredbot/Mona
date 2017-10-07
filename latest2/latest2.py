import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import glob
import os
import aiohttp

class link:
    """A custom cog that will grab the url of the latest upload"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def link(self, ctx):
        """Get the latest download release"""

        #BeautifulSoup
        try:
            list_of_files = glob.glob('http://dd.atelierdunoir.org/*') # * means all if need specific format then *.csv
            download_url = max(list_of_files, key=os.path.getctime)
            return await self.bot.send_message(ctx.message.author, download_url)
        except:
            return await self.bot.send_message(ctx.message.author, "Command was unsuccessful due to error.")
        
def setup(bot):
    bot.add_cog(link(bot))
