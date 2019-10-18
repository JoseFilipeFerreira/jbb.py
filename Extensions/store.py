import discord
from discord.ext import commands
import asyncio
from aux.cash import enough_cash, give_cash, spend_cash, save_stats 
from aux.inventory import get_inventory

class Store(commands.Cog):
    """Spend your money here"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='richest',
            description="get richest users",
            brief="richests users")
    @commands.is_nsfw()
    async def richest(self, ctx):
        embed = discord.Embed(
            title = 'Economy no DI',
            color=self.bot.embed_color)
        embed.set_thumbnail(
            url="http://pixelartmaker.com/art/89daa821cd53576.png") 

        money = []
        for id in self.bot.stats:
            money.append({
                "id": id,
                "cash": self.bot.stats[id]["cash"]})

        money.sort(key=lambda d: d["cash"], reverse=True)

        for i in range(3):
            cash = money[i]
            member = ctx.message.guild.get_member(cash["id"])

            embed.add_field(
                name="{0}. {1}".format(i + 1, member.display_name),
                value="Cash: {0}".format(cash["cash"]),
                inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='market',
            description="Buy things to put in your inventory",
            brief="MiEI Market")
    @commands.is_nsfw()
    async def market(self, ctx, store = None, *,tool = None):
        if not store:
            await market_stalls(self, ctx)
        elif not tool:
            await stall(self, ctx, store)
        elif store and tool:
            await store_interact(self, ctx, store, tool)

async def store_interact(self, ctx, store, tool):
    embed = default_embed(self, ctx)
    store = store.lower()
    prod  = tool.lower()
    if store not in self.bot.market:
        embed.add_field(
            name="Invalid Store",
            value="{0}market to get valid stores".format(self.bot.command_prefix))
        return

    prod_dic =  find(self.bot.market[store]["contents"], "name", prod)
    if prod_dic == None:
        embed.add_field(
            name="Invalid Product",
            value="{0}market {1} to get valid products in this store".format(self.bot.command_prefix, store))
        ctx.send(embed=embed)
        return

    price = prod_dic["cost"]
    if not enough_cash(self.bot, ctx.message.author.id, price):
        embed.add_field(
            name="Not enough money",
            value="Item is too expensive")
        await ctx.send(embed=embed)
        return

    inventory = get_inventory(self.bot, ctx.message.author.id)

    embed.add_field(
        name="{0}{1}".format(
            prod_dic["simbol"],
            prod_dic["name"]),
        value="cost: {0}\nstat: {1}".format(
            prod_dic["cost"],
            prod_dic["stats"]))
    
    embed.add_field(
        name="**Replace**",
        value="{0} {1}\nstat: {2}".format(
            inventory["gear"][store]["simbol"],
            inventory["gear"][store]["name"],
            inventory["gear"][store]["stats"])) 

    embed.set_footer(
        text="select to buy")

    spend_cash(self.bot, ctx.message.author.id, price)
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('\U0000274C')
    await msg.add_reaction('\U00002705')
    
    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in ['\U00002705', '\U0000274C']  
    
    try:
         reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await msg.clear_reactions()
        give_cash(self.bot, ctx.message.author.id, price)
        return

    await msg.clear_reactions()

    if reaction.emoji ==  '\U0000274C':
        give_cash(self.bot, ctx.message.author.id, price)
        return

    for prop in prod_dic.keys():
        inventory["gear"][store][prop] = prod_dic[prop]
    
    await ctx.send("Transaction was successfull")
    save_stats(self.bot)


async def market_stalls(self, ctx):
    embed = default_embed(self, ctx)
    for store in self.bot.market.keys():
        embed.add_field(
            name="{0} {1}".format(
                self.bot.market[store]["simbol"],
                store),
            value=self.bot.market[store]["description"])
    
    embed.set_footer(text="{0}market [store] to see one store".format(self.bot.command_prefix))

    await ctx.send(embed=embed)

async def stall(self, ctx, store):
    embed = default_embed(self, ctx)
    store = store.lower()
    if store in self.bot.market:
        store_items(
            embed,
            self.bot.market[store]["stats"],
            self.bot.market[store]["contents"])
        
        embed.set_footer(
            text="{0}market {1} [tool] to buy from store".format(self.bot.command_prefix, store))
    else:
        embed.add_field(
            name="Invalid Store",
            value="{0}market to get valid stores".format(self.bot.command_prefix))
    await ctx.send(embed=embed)

def store_items(embed, stat, items):
    items.sort(key=lambda i: i["stats"])

    for item in items:    
        embed.add_field(
            name="{0}{1}".format(
                item["simbol"],
                item["name"]),
            value="cost: {2}\n{0}: {1}\n".format(
                stat,
                item["stats"],
                item["cost"]),
            inline=False)

def default_embed(self, ctx):
    embed = discord.Embed(
            title = 'Market de {}'.format(ctx.message.guild.name),
            color=self.bot.embed_color)
    embed.set_thumbnail(
            url="http://pixelartmaker.com/art/9a22f122756ab01.png")
    return embed

def find(arr, key, value):
    for dic in arr:
        if dic[key] == value:
            return dic
    return None

def setup(bot):
    bot.add_cog(Store(bot))
