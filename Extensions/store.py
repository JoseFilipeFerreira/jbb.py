import discord
from discord.ext import commands
import random
from random import randint
from random import choice
import asyncio

class Store():
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='richest',
                      description="get richest users",
                      brief="richests users",
                      pass_context=True)
    async def richest(self, ctx):
        money = []
        embed = discord.Embed(
            title = 'Economy no DI',
            color=self.bot.embed_color)
        
        for id in self.bot.stats:
            money.append({
                "id": id,
                "cash": self.bot.stats[id]["cash"]})
        
        def compare(money):
            return money["cash"]
        money.sort(key=compare, reverse=True)

        for i in range(3):
            cash = money[i]
            member = ctx.message.server.get_member(cash["id"])
            name = member.name
            if member.nick != None:
                name = member.nick

            embed.add_field(
                name="{0}. {1}".format(i + 1, name),
                value="Cash: {0}".format(cash["cash"]),
                inline=False
            )
        embed.set_thumbnail(
                url="http://pixelartmaker.com/art/89daa821cd53576.png") 

        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Store(bot))
