import discord
from discord.ext import commands
import asyncio
import wolframalpha
from aiohttp import ClientSession
from html2text import html2text
from random import choice, randint
from re import sub
import urllib


class Api(commands.Cog):
    """Get random cute pics"""

    def __init__(self, bot):
        self.bot = bot
        self.client = wolframalpha.Client(bot.config['credentials']['wolframalpha'])
        self.colours = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a]

    @commands.command(name='ask',
                      description="replies to a query with the short text answer of the wolfram alpha API",
                      brief="wolfram alpha API")
    async def ask(self, ctx, *, query):
        res = self.client.query(query)
        if res['@success'] == 'false':
            strRes = "Couldn't find an answer"
        else:
            strRes = next(res.results).text
        embed = discord.Embed(
            title=query,
            description=strRes,
            color=self.bot.embed_color)
        await ctx.send(embed=embed)

    @commands.command(name='dog',
                      description="send random dog picture",
                      brief="send dog pic",
                      aliases=['auau'])
    async def dog(self, ctx):
        while True:
            result, error = await get_json('https://random.dog/woof.json')
            if error:
                await ctx.send(error)
                return
            if result['url'].endswith('.mp4'):
                pass
            else:
                embed = discord.Embed(color=choice(self.colours))
                embed.set_image(url=result['url'])
                await ctx.send(embed=embed)
                return

    @commands.command(name='cat',
                      description="send random cat picture",
                      brief="send cat pic",
                      aliases=['antiauau', 'miau'])
    async def cat(self, ctx):
        result, error = await get_json('http://aws.random.cat/meow')
        if error:
            await ctx.send(error)
            return
        embed = discord.Embed(color=choice(self.colours))
        embed.set_image(url=result['file'])
        await ctx.send(embed=embed)

    @commands.command(name='xkcd',
                      brief="send xkcd comic")
    async def xkcd(self, ctx, args = None):
        """
        send xkcd comic
        *xkcd -> sends newest comic
        *xkcd random -> sends random comic
        *xkcd [number] -> sends a specific comic
        """
        url = None
        if not args:
            url = 'http://xkcd.com/info.0.json'
        elif args.isdigit():
            url = f'http://xkcd.com/{int(args)}/info.0.json'
        elif args.lower() == 'random':
            result, error = await get_json('http://xkcd.com/info.0.json')
            if error:
                await ctx.send(error)
                return
            number = randint(0, result['num'])
            url = f'http://xkcd.com/{number}/info.0.json'

        result, error = await get_json(url)
        if error:
            await ctx.send(error)
            return
        embed = discord.Embed(color=choice(self.colours))
        embed.set_image(url=result['img'])
        await ctx.send(embed=embed)

    @commands.command(name='lmgtfy',
                      description="give link for let me google that for you",
                      brief="let me google that for you")
    async def lmgtfy(self, ctx, *query):
        await ctx.send(f"http://lmgtfy.com/?q={urllib.quote(query)}")

    @commands.command(name='lmddgtfy',
                      description="give link for let me duck duck go that for you",
                      brief="let me duck duck go that for you")
    async def lmddgtfy(self, ctx, *query):
        await ctx.send(f"http://lmddgtfy.net/?q={urllib.quote(query)}")


    @commands.command(name='urban',
                      description="Get a urban defenition of a query",
                      brief="search urban")
    async def urban(self, ctx, * query : str):
        url = f"http://api.urbandictionary.com/v0/define?term={'+'.join(query)}"
        result, error = await get_json(url)
        if error:
            await ctx.send(error)
            return
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

    @commands.command(name='hoogle',
                      brief="search hoogle")
    async def hoogle(self, ctx, * query : str):
        """Searches Hoggle and returns first two options
        Click title to see full search"""
        url = f"https://hoogle.haskell.org?mode=json&hoogle={'+'.join(query)}&start=1&count=1"
        result, error = await get_json(url)
        if error:
            await ctx.send(error)
            return
        embed = discord.Embed(
            title=f"Definition of {' '.join(query)}",
            url=f"https://hoogle.haskell.org/?hoogle={'+'.join(query)}",
            color=self.bot.embed_color)
        embed.set_thumbnail(
            url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Lambda-letter-lowercase-symbol-Garamond.svg/1200px-Lambda-letter-lowercase-symbol-Garamond.svg.png")
        if not result:
            embed.add_field(
                    name = "No results found",
                    value="*undefined*",
                    inline=False)
        else:
            for l in result:
                val = "*Module:* " + l["module"]["name"] + "\n"
                val+= sub(r'\n{2,}', '\n\n', sub(r"\n +", "\n" , html2text(l["docs"])))
                embed.add_field(
                    name= html2text(l["item"]),
                    value= val,
                    inline=False)
            embed.set_footer(text="first option in Hoogle (Click title for more)")
        await ctx.send(embed=embed)

async def get_json(url):
    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
        return result, None
    except:
        return None, "Something unexpected went wrong."


def setup(bot):
    bot.add_cog(Api(bot))
