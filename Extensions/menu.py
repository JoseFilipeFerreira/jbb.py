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

    @commands.command(pass_context=True)
    async def helpPlay(self, ctx):
        await MenuGenerateEmbed(self, ctx, self.bot.musicMap,"Music", "available music in jukebox:")

    @commands.command(pass_context=True)
    async def helpImage(self, ctx):
        await MenuGenerateEmbed(self, ctx, self.bot.imagesMap,"Image", "available memes and photos:")

    @commands.command(pass_context=True)
    async def helpGif(self, ctx):
        await MenuGenerateEmbed(self, ctx, self.bot.gifsMap,"Gif", "available Gif/Jif:")


async def MenuGenerate(self, ctx, name):
    with open('./modules/menus.json') as menusFile:
            menus = json.load(menusFile)
            await self.bot.send_message(ctx.message.author, menus[name])
            await self.bot.delete_message(ctx.message)

async def MenuGenerateEmbed(self, ctx, thingMap, title, section):

    embed=discord.Embed(
        title=title,
        description=" ",
        color=self.bot.embed_color
    )
    musicArray = []
    for music in thingMap:
        musicArray.append(music)
    musicArray.sort()
    embed.add_field(name=section, value='\n'.join(musicArray), inline=True)
    await self.bot.send_message(ctx.message.author, embed=embed)
    await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(Menu(bot))