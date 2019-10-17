import discord
from discord.ext import commands
import asyncio
import requests
from random import choice

class Dogs(commands.Cog):
    """Get random cute pics"""
    
    def __init__(self, bot):
        self.bot = bot
        self.colours = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a]

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
    bot.add_cog(Dogs(bot))
