import discord
from baseconvert import base
from discord.ext import commands
from random import randint

class Programming():
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command(pass_context=True)
    async def helpHaskell(self, ctx):
        await self.bot.say('```Haskell\ndouble :: Double -> Double\ndouble x = x + x```')
    

    @commands.command(pass_context=True)
    async def helpC(self, ctx):
        await self.bot.say('```C\nint main()\n{\n    printf("wololo");\n    return 0;\n}\n```')


    @commands.command(pass_context=True)
    async def conv(self, ctx, n, basefrom, baseto):
        result = base(n, int(basefrom), int(baseto), string=True)
        await self.bot.say(
            n + ' na base ' + basefrom + ' para base ' + baseto + ' dá:\n' + result)



def setup(bot):
    bot.add_cog(Programming(bot))        