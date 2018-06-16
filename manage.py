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

#    @commands.command(pass_context=True)
#    async def vote(self, ctx):
#        timeBUP = 10
#        if "Administrador" in [y.name for y in ctx.message.author.roles]:
#            vote = await self.bot.say('Vote here')
#            await self.bot.add_reaction(vote, '\U0000274C')
#            await self.bot.add_reaction(vote, '\U00002705')
#            nupdates = 5*60/timeBUP
#            while nupdates > 0:
#                time.sleep(timeBUP)
#                vote = await self.bot.get_message(vote.channel, vote.id)
#                status = '(Tied)'
#                nX = 0
#                ncheck = 0
#                for reaction in vote.reactions:
#                    if reaction.emoji == '\U0000274C':
#                        reactors = await self.bot.get_reaction_users(reaction)
#                        for reactor in reactors:
#                            nX = nX +1
#                    elif reaction.emoji == '\U00002705':
#                        reactors = await self.bot.get_reaction_users(reaction)
#                        for reactor in reactors:
#                            ncheck = ncheck + 1
#                if ncheck == 1 and nX == 1 : status = ' '
#                elif ncheck > nX: status = '(Yes is wining)'
#                elif ncheck < nX: status = '(No is wining)'
#                await self.bot.edit_message(vote, 'Vote here {}'.format(status))
#                nupdates = nupdates -1
#                print(nupdates)
#            vote = await self.bot.get_message(vote.channel, vote.id)
#            status = '(Tied)'
#            nX = 0
#            ncheck = 0
#            for reaction in vote.reactions:
#                if reaction.emoji == '\U0000274C':
#                    reactors = await self.bot.get_reaction_users(reaction)
#                    for reactor in reactors: nX = nX +1
#                elif reaction.emoji == '\U00002705':
#                    reactors = await self.bot.get_reaction_users(reaction)
#                    for reactor in reactors: ncheck = ncheck + 1
#            if ncheck == 1 and nX == 1 : status = ' '
#            elif ncheck > nX: status = '(Yes won)'
#            elif ncheck < nX: status = '(No won)'
#            await self.bot.edit_message(vote, 'Vote here {}'.format(status))
#        else:
#            await self.bot.say("Invalid User")



    #@commands.command(pass_context=True)
    #async def test(self, ctx):
    #    if "Administrador" in [y.name for y in ctx.message.author.roles]:
    #        await self.bot.add_reaction(ctx.message, '\U0001F44D')



def setup(bot):
    bot.add_cog(Manage(bot))
