import discord
from discord.ext import commands
import aiohttp
import asyncio
import requests
import wolframalpha
from random import choice

#setup wolframalpha API
client = wolframalpha.Client(open('WA_KEY').readline().rstrip())

class Api(commands.Cog):
    """Get random cute pics"""
    
    def __init__(self, bot):
        self.bot = bot
        self.colours = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a]

    @commands.command(name='ask',
                      description="replies to a query with the short text answer of the wolfram alpha API",
                      brief="wolfram alpha API")
    async def ask(self, ctx, *, query):
        res = client.query(query)
        if res['@success'] == 'false':
            strRes = "Couldn't find an answer"
        else:
            strRes = next(res.results).text
        embed = discord.Embed(
            title=query,
            description=strRes,
            color=self.bot.embed_color)
        await ctx.send(embed=embed)

    @commands.command(name='lmgtfy',
                      description="give link for let me google that for you",
                      brief="let me google that for you")
    async def lmgtfy(self, ctx, *query):
        await ctx.send(f"http://lmgtfy.com/?q={'+'.join(word for word in query)}")

    @commands.command(name='urban',
                      description="Get a urban defenition of a query",
                      brief="search urban")
    async def urban(self, ctx, * query : str):
        url = "http://api.urbandictionary.com/v0/define?term=" + "+".join(query)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    result = await response.json()
            if result["list"]:
                top_def = result['list'][0]

                embed = discord.Embed(
                    title=f"Definition of {top_def['word']}",
                    url=top_def['permalink'],
                    description=top_def['definition'],
                    color=self.bot.embed_color)
                
                embed.set_thumbnail(
                    url = "http://campbelllawobserver.com/wp-content/uploads/2014/03/Urban-Dictionary-e1372286057646.png")

                embed.add_field(
                    name="Example",
                    value=top_def['example'],
                    inline=False)
                embed.add_field(
                    name=":thumbsup:",
                    value=top_def['thumbs_up'],
                    inline=True)
                embed.add_field(
                    name=":thumbsdown:",
                    value=top_def['thumbs_down'],
                    inline=True)
                
                embed.set_footer(text=f"Submited by {top_def['author']}")

                await ctx.send(embed =embed)
            else:
                await ctx.send("Your query gave no results.")
        except:
            await self.bot.say("Something unexpected went wrong.")

    @commands.command(name='dog',
                      description="send random dog picture",
                      brief="send dog pic",
                      aliases=['auau'])
    async def dog(self, ctx):
        while True:
            r = requests.get('https://random.dog/woof.json')
            js = r.json()
            if js['url'].endswith('.mp4'):
                pass
            else:
                embed = discord.Embed(color=choice(self.colours))
                embed.set_image(url=js['url'])
                await ctx.send(embed=embed)
                return

    @commands.command(name='cat',
                      description="send random cat picture",
                      brief="send cat pic",
                      aliases=['antiauau', 'miau'])
    async def cat(self, ctx):
        r =requests.get('http://aws.random.cat/meow')
        embed = discord.Embed(color=choice(self.colours))
        embed.set_image(url=r.json()['file'])
        await ctx.send(embed=embed) 

def setup(bot):
    bot.add_cog(Api(bot))
