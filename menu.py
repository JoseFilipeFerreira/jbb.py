import discord
import json
from discord.ext import commands


class Menu():
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, ctx):
        with open('./package.json') as menusFile:
            info = json.load(menusFile)
            await self.bot.say('**' + info['description'] + '**\n\nCreated by: *' + info['author'] + '*\nVersion: *' + info['version'] + '*\n\n`*help` for commands')
    
    
    @commands.command(pass_context=True)
    async def help(self, ctx):
        with open('./modules/menus.json') as menusFile:
            menus = json.load(menusFile)
            await self.bot.send_message(ctx.message.author, menus['help'])
            await self.bot.delete_message(ctx.message)
    
    
    @commands.command(pass_context=True)
    async def helpP(self, ctx):
        with open('./modules/menus.json') as menusFile:
            menus = json.load(menusFile)
            await self.bot.send_message(ctx.message.author, menus['helpP'])
            await self.bot.delete_message(ctx.message)
    
    
    @commands.command(pass_context=True)
    async def helpG(self, ctx):
        with open('./modules/menus.json') as menusFile:
            menus = json.load(menusFile)
            await self.bot.send_message(ctx.message.author, menus['helpG'])
            await self.bot.delete_message(ctx.message)
    
    
    @commands.command(pass_context=True)
    async def helpquote(self, ctx):
        with open('./modules/menus.json') as menusFile:
            menus = json.load(menusFile)
            await self.bot.send_message(ctx.message.author, menus['helpquote'])
            await self.bot.delete_message(ctx.message)
    
    @commands.command(pass_context=True)
    async def sudohelp(self, ctx):
        if "Administrador" in [y.name for y in ctx.message.author.roles]:
            with open('./modules/menus.json') as menusFile:
                menus = json.load(menusFile)
                await self.bot.send_message(ctx.message.author, menus['sudohelp'])
                await self.bot.delete_message(ctx.message)
        else:
            await self.bot.say('Invalid user')


#@bot.command(pass_context=True)
#async def helpPlay(ctx):
#    with open('./modules/menus.json') as menusFile:
#        menus = json.load(menusFile)
#        await bot.say(menus['helpPlay'] + musicFiles.join('\n'))

def setup(bot):
    bot.add_cog(Menu(bot))