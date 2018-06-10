import discord
import json
import subprocess
from discord.ext import commands

class Manage():
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def update(self, ctx):
        appInfo = await self.bot.application_info()
        if ctx.message.author == appInfo.owner:
            subprocess.call("./update.sh") 
   

def setup(bot):
    bot.add_cog(Manage(bot))