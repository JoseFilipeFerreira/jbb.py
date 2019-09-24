import discord
from discord.ext import commands
import asyncio
from aux.cash import enough_cash, give_cash, spend_cash, save_stats 
from aux.inventory import get_inventory

class Store(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='richest',
            description="get richest users",
            brief="richests users")
    @commands.is_nsfw()
    async def richest(self, ctx):
        money = []
        embed = discord.Embed(
            title = 'Economy no DI',
            color=self.bot.embed_color)
        embed.set_thumbnail(
            url="http://pixelartmaker.com/art/89daa821cd53576.png") 

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

            embed.add_field(
                name="{0}. {1}".format(i + 1, member.display_name),
                value="Cash: {0}".format(cash["cash"]),
                inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='market',
            description="Buy things to put in your iventory",
            brief="MiEI Market")
    #@commands.is_nsfw()
    async def market(self, ctx, store = None, *,tool = None):
        embed = discord.Embed(
                title = 'Market de {}'.format(ctx.message.guild.name),
                color=self.bot.embed_color)

        embed.set_thumbnail(
                url="http://pixelartmaker.com/art/9a22f122756ab01.png")

        if not store:
            for store in self.bot.market.keys():
                embed.add_field(
                    name="{0} {1}".format(
                        self.bot.market[store]["simbol"],
                        store),
                    value=self.bot.market[store]["description"])
            
            embed.set_footer(text="*market [store] to see one store")

            await ctx.send(embed=embed)
        
        elif not tool:
            store = store.lower()
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
            await ctx.send(embed=embed)

        elif store and tool:
            store = store.lower()
            prod  = tool.lower()
            if store not in self.bot.market:
                                embed.add_field(
                    name="Invalid Store",
                    value="*market to get valid stores")
            else:
                prod_dic =  find(self.bot.market[store]["contents"], "name", prod)
                if prod_dic == None:
                    embed.add_field(
                        name="Invalid Product",
                        value="*market {0} to get valid products in this store".format(store))
                else:
                    price = prod_dic["cost"]
                    inventory = get_inventory(self.bot, ctx.message.author.id)
                    if not enough_cash(self.bot, ctx.message.author.id, price):
                        embed.add_field(
                            name="Not enough money",
                            value="Item is too expensive")
                        await ctx.send(embed=embed)
                    else:
                        embed.add_field(
                            name="{0}{1}".format(
                                prod_dic["simbol"],
                                prod_dic["name"]),
                            value="cost: {0}\nstat: {1}".format(
                                prod_dic["cost"],
                                prod_dic["stat"]))
        
                        embed.add_field(
                            name="**Replace**",
                            value="{0} {1}\nstat: {2}".format(
                                inventory["gear"][store]["simbol"],
                                inventory["gear"][store]["name"],
                                inventory["gear"][store]["stats"])) 

                        embed.set_footer(
                            text="[yes/no] to buy")

                        spend_cash(self.bot, ctx.message.author.id, price)
                        
                        await ctx.send(embed=embed)

                        def guess_check(m):
                             return m.content.lower() == 'yes' or m.content.lower() == 'no'
        
                        answer = await self.bot.wait_for_message(
                            timeout=10.0,
                            author=ctx.message.author,
                            check=guess_check)
            
                        if answer is None:
                            give_cash(self.bot, ctx.message.author.id, price)
                            return
                        elif answer.content.lower() == 'no':
                            give_cash(self.bot,ctx.message.author.id, price)
                            return
                        
                        inventory["gear"][store]["simbol"] = prod_dic["simbol"]
                        inventory["gear"][store]["name"]   = prod_dic["name"]
                        inventory["gear"][store]["stats"]  = prod_dic["stat"]
                        
                        await ctx.send("Transaction was successfull")
                        save_stats(bot)

def store_items(embed, stat, items):
    def compare(item):
        return item["stat"]
    items.sort(key=compare)

    for item in items:    
        embed.add_field(
            name="{0}{1}".format(
                item["simbol"],
                item["name"]),
            value="cost: {2}\n{0}: {1}\n".format(
                stat,
                item["stat"],
                item["cost"]),
            inline=False)

def find(arr, key, value):
    for dic in arr:
        if dic[key] == value:
            return dic
    return None

def setup(bot):
    bot.add_cog(Store(bot))
