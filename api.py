import discord
import wolframalpha
from baseconvert import base
from discord.ext import commands
from random import randint

client = wolframalpha.Client(open('WA_KEY').readline().rstrip())

class Api():
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def ask(self, ctx):
        query = ctx.message.content[5:]
        res = client.query(query)
        if res['@success'] == 'false':
            strRes = "Couldn't find an answer"
        else:
            strRes = next(res.results).text
            
        answer = '**' + query +'**' + '\n```' + strRes + '```'
        await self.bot.say(answer)



def setup(bot):
    bot.add_cog(Api(bot))