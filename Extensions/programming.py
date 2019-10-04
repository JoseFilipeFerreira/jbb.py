import discord
from baseconvert import base
from discord.ext import commands
from random import randint
import requests 

class Programming(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name='helpHaskell',
                      description="give overlycomplicated function that returns the double of a given number in haskell",
                      brief="small program in haskell")
    async def helpHaskell(self, ctx):
        doublFct = ['double = foldr (+) 0 . take 2 . repeat', 
            'double = foldr (+) 0 . take 2 . cycle . return',
            'double = head . fmap ap . zip [(2*)] . return',
            'double = succ . (!!2) . enumFromThen 1',
            'double = uncurry (+) . dup',
            'double x = x + x']
        await ctx.send('```Haskell\ndouble :: Double -> Double\n' + doublFct[randint(0, len(doublFct) - 1)] + '```')

    @commands.command(name='quicksort',
                      description="help understand quicksort",
                      brief="quicksort is hard guys")
    async def quicksort(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=ywWBy6J5gz8')

    @commands.command(name='conv',
                      description="convert between numeric bases",
                      brief="convert between bases")
    async def conv(self, ctx, number, basefrom : int, baseto :int ):
        result = base(number, basefrom, baseto, string=True)
        await ctx.send('{0} na base {1} para base {2} dá:\n{3}'
                .format(number, basefrom, baseto, result))

    @commands.command(name='lmgtfy',
                      description="give link for let me google that for you",
                      brief="let me google that for you")
    async def lmgtfy(self, ctx, *query):
        query = '+'.join(word for word in query)
        await ctx.send("http://lmgtfy.com/?q={0}".format(query))
    
def setup(bot):
    bot.add_cog(Programming(bot))     

