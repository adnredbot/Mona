import discord
from discord.ext import commands
import os, time
from ftplib import FTP
from bs4 import BeautifulSoup
import aiohttp

ftp = FTP('ftp.aphelion.gq')     # connect to host, default port
ftp.login("redbot@dd.atelierdunoir.org", "2fwg84phzdcf")

ftp.set_pasv('true')
# list files with ftplib
file_list = ftp.nlst()

class link:
    """A custom cog that will grab the url of the latest upload"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def link(self, ctx):
        """Get the latest download release"""

        #BeautifulSoup
        url = "http://dd.atelierdunoir.org/" #get the web url
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser" )
        try:
            download_url = soupObject.find('a')['href']
            return await self.bot.send_message(ctx.message.author, download_url)
        except:
            return await self.bot.send_message(ctx.message.author, "Command was unsuccessful due to error.")
        
def setup(bot):
    bot.add_cog(link(bot))
