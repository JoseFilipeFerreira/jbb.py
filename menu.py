import discord
import json
from discord.ext import commands


class Menu():
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def help(self, ctx):
        await MenuGenerate(self, ctx, 'help')
    
    @commands.command(pass_context=True)
    async def helpP(self, ctx):
        await MenuGenerate(self, ctx, 'helpP') 
    
    @commands.command(pass_context=True)
    async def helpG(self, ctx):
        await MenuGenerate(self, ctx, 'helpG')  
    
    @commands.command(pass_context=True)
    async def helpquote(self, ctx):
        await MenuGenerate(self, ctx, 'helpquote')
    
    @commands.command(pass_context=True)
    async def sudohelp(self, ctx):
        if "Administrador" in [y.name for y in ctx.message.author.roles]:
            await MenuGenerate(self, ctx, 'sudohelp')
        else:
            await self.bot.say('Invalid user')

async def MenuGenerate(self, ctx, name):
    with open('./modules/menus.json') as menusFile:
            menus = json.load(menusFile)
            await self.bot.send_message(ctx.message.author, menus[name])
            await self.bot.delete_message(ctx.message)


#@bot.command(pass_context=True)
#async def helpPlay(ctx):
#    with open('./modules/menus.json') as menusFile:
#        menus = json.load(menusFile)
#        await bot.say(menus['helpPlay'] + musicFiles.join('\n'))

def setup(bot):
    bot.add_cog(Menu(bot))