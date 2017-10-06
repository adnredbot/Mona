import discord
from discord.ext import commands
import ftplib
from cogs.utils.dataIO import dataIO
import os
from .utils import checks
from __main__ import send_cmd_help
import asyncio
from bs4 import BeautifulSoup
import aiohttp

class latest:
    """A custom cog that will grab the url of the latest upload"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ftp(self, ctx):
        """Get the latest download release"""

        #BeautifulSoup
        url = "http://atelierdunoir.org/contemplations/" #get the web url
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser" )
        try:
            download_url = soupObject.find(class_='release-download-icons').find_all('li')[1].find('a')['href']
            return await self.bot.send_message(ctx.message.author, download_url)
        except:
            return await self.bot.send_message(ctx.message.author, "Command was unsuccessful due to error.")
        
def setup(bot):
    bot.add_cog(latest(bot))
