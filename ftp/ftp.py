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

class FTPStats:
    """Uploads server statistics to an ftp server!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/ftpstats/settings.json")
        self.stats = dataIO.load_json("data/ftpstats/stats.json")
        
    @commands.group(name="ftpset", pass_context=True)
    @checks.is_owner()
    async def ftpset(self, ctx):
        """Manage all ftpstats settings"""
        if not ctx.invoked_subcommand:
            await send_cmd_help(ctx)
            
    @ftpset.command()
    @checks.is_owner()
    async def server(self, server):
        """Set the server for the ftp stats. Has to be a link
        
        example:
        [p]ftpset server ftp.yoursite.com
        DON'T ADD FTP://!"""
        self.settings['ftp_server'] = server
        dataIO.save_json("data/ftpstats/settings.json", self.settings)
        await self.bot.say("Done!")
    

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
