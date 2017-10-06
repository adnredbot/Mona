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
        
        
    @ftpset.command()
    @checks.is_owner()
    async def username(self, username):
        """Sets the username to log in to the server."""
        self.settings['ftp_username'] = username
        dataIO.save_json("data/ftpstats/settings.json", self.settings)
        await self.bot.say("Done!")

    @ftpset.command(pass_context=True)
    @checks.is_owner()
    async def password(self, ctx, password):
        """Sets the password to log in to the server, 
        for security it only works in Direct Messages"""
        if ctx.message.server is not None:
            try:
                self.bot.delete_message(ctx.message)
            except:
                pass
            await self.bot.say("Direct messages only please, security reasons.")
        else:
            self.settings['ftp_password'] = password
            dataIO.save_json("data/ftpstats/settings.json", self.settings)
            await self.bot.say("Done!")

    @ftpset.command()
    @checks.is_owner()
    async def defaultdir(self, dir):
        """Set a directory to which the bot should upload the files 
        (stats for every server are in it's own folder.)"""
        self.settings['ftp_defaultdir'] = dir
        dataIO.save_json("data/ftpstats/settings.json", self.settings)
        await self.bot.say("Done!")

    @ftpset.command()
    @checks.is_owner()
    async def start(self):
        """Start uploading the stats to the ftp server."""
        # Setting up
        if self.settings['ftp_server'] is None:
            await self.bot.say("Your ftp settings are not set yet, you can set them with [p]ftpset")
            return
        else:
            if self.settings['ftp_password'] is None:
                self.settings['ftp_password'] = "anonymous@"
            try:
                ftp = ftplib.FTP(self.settings['ftp_server'])
            except:
                await self.bot.say("Can't connect to the FTP server, are you sure you didn't add ftp:// to the beginning?\nThis error is not because of your password or username though.")
                return
            try:
                ftp.login(self.settings['ftp_username'], self.settings['ftp_password'])
            except:
                await self.bot.say("Can't login to the FTP server, are you sure your login credentials are correct?\nThe ip is correct though.")
                return
            if self.settings['ftp_defaultdir'] is not None:
                ftp.cwd(self.settings['ftp_defaultdir'])
            self.settings['ftp_started'] = True
            dataIO.save_json("data/ftpstats/settings.json", self.settings)
            await self.bot.say("Succesfully connected!")

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
        
def check_folders():
    if not os.path.exists("data/ftpstats"):
        print("Creating data/ftpstats folder...")
        os.makedirs("data/ftpstats")
        
def check_files():
    if not os.path.exists("data/ftpstats/settings.json"):
        print("Creating data/ftpstats/settings.json file...")
        dataIO.save_json("data/ftpstats/settings.json", {'ftp_server': None, 'ftp_username': None, 'ftp_password': "anonymous@", 'ftp_defaultdir': None})
    if not os.path.exists("data/ftpstats/stats.json"):
        print("Creating data/ftpstats/stats.json file...")
        dataIO.save_json("data/ftpstats/stats.json", {})        
        
def setup(bot):
    check_folders()
    check_files()
    cog = FTPStats(bot)
    bot.add_cog(cog)
