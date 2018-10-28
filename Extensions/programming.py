import discord
import matplotlib.pyplot as plt
import numpy as np
from baseconvert import base
from discord.ext import commands
from random import randint
from math import *

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

    @commands.command(pass_context=True)
    async def draw(self, ctx, xmax : int, *, formula):
    #draw graph
    
        env = {}
        env["__import__"] = None

        if (xmax < 1 or xmax > 101):
            await self.bot.say("Invalid dimensions")
            return
        await self.bot.delete_message(ctx.message)

        tests = np.arange(0.0, xmax, 0.01)
        s = []
        t = []
        for x in tests:
            try:
                result = eval(formula, env)
                s.append(result)
                t.append(x)
            except Exception:
                pass
        plt.plot(t, s)

        plt.xlabel("X")
        plt.ylabel(formula)
        plt.title("Plot requested by "+ctx.message.author.name)

        fig = plt.gcf()
        fig.savefig(self.bot.TMP_PATH + "plot.png")
        await self.bot.send_file(ctx.message.channel, self.bot.TMP_PATH + "plot.png")
        plt.close()

def setup(bot):
    bot.add_cog(Programming(bot))        
