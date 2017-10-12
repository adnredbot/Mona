import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp

class batoto:
    """A custom cog that will grab the url of the latest upload"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def batoto(self, ctx):
        """Get the latest download release"""

        #BeautifulSoup
        url = "http://atelierdunoir.org/reader/" #get the web url
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser" )
        try:
            download_url = soup.find( "table", {"class":"ipb_table chapters_list"} )
            rows=list()
            for row in table.findAll("tr").find('a')['href']:
            rows.append(row)
            return await self.bot.send_message(ctx.message.author, download_url)
        except:
            return await self.bot.send_message(ctx.message.author, "Command was unsuccessful due to error.")
        
def setup(bot):
    bot.add_cog(batoto(bot))
