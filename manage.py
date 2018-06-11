import discord
import time
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
            await self.bot.change_presence(game=discord.Game(name='rebooting'))
            subprocess.call("./update.sh")
        else:
            wait self.bot.say("Invalid User")
    
    @commands.command(pass_context=True)
    async def stdplay(self, ctx):
        appInfo = await self.bot.application_info()
        if ctx.message.author == appInfo.owner:
            await self.bot.change_presence(game=discord.Game(name='*help'))
        else:
            wait self.bot.say("Invalid User")

def setup(bot):
    bot.add_cog(Manage(bot))
