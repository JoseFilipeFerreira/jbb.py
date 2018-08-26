import discord
from baseconvert import base
from discord.ext import commands
from random import randint

class Programming():
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command(pass_context=True)
    async def helpHaskell(self, ctx):
    #give overlycomplicated function that returns the double of a given number in haskell
        doublFct = ['double = foldr (+) 0 . take 2 . repeat', 
            'double = foldr (+) 0 . take 2 . cycle . return',
            'double = head . fmap ap . zip [(2*)] . return',
            'double = succ . (!!2) . enumFromThen 1',
            'double = uncurry (+) . dup',
            'double x = x + x']
        await self.bot.say('```Haskell\ndouble :: Double -> Double\n' + doublFct[randint(0, len(doublFct) - 1)] + '```')


    @commands.command(pass_context=True)
    async def helpC(self, ctx):
    #give simple function in C
        await self.bot.say('```C\nint main()\n{\n    printf("wololo");\n    return 0;\n}\n```')


    @commands.command(pass_context=True)
    async def conv(self, ctx, n, basefrom, baseto):
    #converter entre bases
        result = base(n, int(basefrom), int(baseto), string=True)
        await self.bot.say(
            n + ' na base ' + basefrom + ' para base ' + baseto + ' dá:\n' + result)

    @commands.command(pass_context=True)
    async def lmgtfy(self, ctx, *query):
    #returns a link for the website "let me google that for you" with the query given
        query = '+'.join(word for word in query)
        await self.bot.say("http://lmgtfy.com/?q={}".format(query))


def setup(bot):
    bot.add_cog(Programming(bot))        
