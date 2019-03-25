import discord
from baseconvert import base
from discord.ext import commands
from random import randint
import requests 

class Programming():
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name='helpHaskell',
                      description="give overlycomplicated function that returns the double of a given number in haskell",
                      brief="small program in haskell",
                      pass_context=True)
    async def helpHaskell(self, ctx):
        doublFct = ['double = foldr (+) 0 . take 2 . repeat', 
            'double = foldr (+) 0 . take 2 . cycle . return',
            'double = head . fmap ap . zip [(2*)] . return',
            'double = succ . (!!2) . enumFromThen 1',
            'double = uncurry (+) . dup',
            'double x = x + x']
        await self.bot.say('```Haskell\ndouble :: Double -> Double\n' + doublFct[randint(0, len(doublFct) - 1)] + '```')


    @commands.command(name='helpC',
                      description="give simple function in C",
                      brief="small program in C",
                      pass_context=True)
    async def helpC(self, ctx):
        await self.bot.say('```C\nint main()\n{\n    printf("wololo");\n    return 0;\n}\n```')


    @commands.command(name='conv',
                      description="convert between numeric bases",
                      brief="convert between bases",
                      pass_context=True)
    async def conv(self, ctx, number, basefrom, baseto):
        result = base(number, int(basefrom), int(baseto), string=True)
        await self.bot.say(
            number + ' na base ' + basefrom + ' para base ' + baseto + ' dá:\n' + result)

    @commands.command(name='lmgtfy',
                      description="give link for let me google that for you",
                      brief="let me google that for you",
                      pass_context=True)
    async def lmgtfy(self, ctx, *query):
        query = '+'.join(word for word in query)
        await self.bot.say("http://lmgtfy.com/?q={}".format(query))
    
    @commands.command(name='lixo3',
                      description="answer querys LI3",
                      brief="answer querys LI3",
                      pass_context=True)
    async def lixo3(self, ctx, *query):
        with open(self.bot.IP_PATH, 'r') as file:
            ip = file.read().strip()
        query = '/'.join(word for word in query)

        await self.bot.send_message(ctx.message.author, "**{0}**".format(query))

        r = requests.get("http://{}/{}".format(ip, query)).text
        r = r.split('\n')
        
        buf = ""
        for m in r:
            if len(buf) + len(m + "\n") > 1900:
                await self.bot.send_message(ctx.message.author, buf)
                buf = m + "\n"
            else:
                buf += (m + "\n") 

    async def copy(self, ctx ,*, text):
        with open(self.bot.IP_PATH, 'w') as file:
            file.write(text)


def setup(bot):
    bot.add_cog(Programming(bot))        
