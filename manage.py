import discord
import json
import subprocess
import time
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
            await self.bot.say("Invalid User")
    
    @commands.command(pass_context=True)
    async def setplay(self, ctx, *playing):
        if "Administrador" in [y.name for y in ctx.message.author.roles]:
            play = ' '.join(word for word in playing)
            appInfo = await self.bot.application_info()
            await self.bot.change_presence(game=discord.Game(name=play))
        else:
            await self.bot.say("Invalid User")

    @commands.command(pass_context=True)
    async def faketype(self, ctx, *playing):
        if "Administrador" in [y.name for y in ctx.message.author.roles]:
            await self.bot.delete_message(ctx.message)
            await self.bot.send_typing(ctx.message.channel)
        else:
            await self.bot.say("Invalid User")


    @commands.command(pass_context=True)
    async def info(self, ctx):
        for user in ctx.message.mentions:
            member = ctx.message.server.get_member(user.id)
            embed = discord.Embed(title=str(user), url=user.avatar_url, description=user.display_name, color=0xffff00)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name='Is bot:', value=user.bot, inline=True)
            embed.add_field(name='Voice channel:', value=user.voice_channel, inline=True)
            embed.add_field(name='Playing:', value=member.game, inline=False)
            embed.add_field(name='Joined discord at:', value=user.created_at, inline=True)
            embed.add_field(name='Joined server at:', value=member.joined_at, inline=True)
            await self.bot.say(embed=embed)




def setup(bot):
    bot.add_cog(Manage(bot))
