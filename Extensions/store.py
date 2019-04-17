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
                    inline=False)

            embed.set_thumbnail(
                    url="http://pixelartmaker.com/art/89daa821cd53576.png") 

            await self.bot.say(embed=embed)

    @commands.command(name='market',
            description="Buy things to put in your iventory",
            brief="MiEI Market",
            pass_context=True)
    async def market(self, ctx, *arg):
        embed = discord.Embed(
                title = 'Market de {}'.format(ctx.message.server.name),
                color=self.bot.embed_color)

        embed.set_thumbnail(
                url="http://pixelartmaker.com/art/9a22f122756ab01.png")

        if len(arg) == 0:
            for store in self.bot.market.keys():
                embed.add_field(
                    name="{0} {1}".format(
                        self.bot.market[store]["simbol"],
                        store),
                    value=self.bot.market[store]["description"])
            
            embed.set_footer(text="*market [store] to see one store")
        
        if len(arg) == 1:
            store = arg[0].lower()
            if store in self.bot.market:
                store_items(
                    embed,
                    self.bot.market[store]["stat"],
                    self.bot.market[store]["contents"])
                
                embed.set_footer(
                    text="*market {0} [tool] to buy from store".format(store))
            else:
                embed.add_field(
                    name="Invalid Store",
                    value="*market to get valid stores")
        
        await self.bot.say(embed=embed)

def store_items(embed, stat, items):
    def compare(item):
        return item["stat"]
    items.sort(key=compare)

    for item in items:    
        embed.add_field(
            name="{0}{1}".format(
                item["simbol"],
                item["name"]),
            value="{0} -> {1}\ncost -> {2}".format(
                stat,
                item["stat"],
                item["cost"]))

def setup(bot):
    bot.add_cog(Store(bot))
