import json
import discord
from discord.ext import commands
from aux.message import user_input_bool
from aux.stats import Gear

class Store(commands.Cog):
    """Spend your money here"""
    def __init__(self, bot):
        self.bot = bot
        with open(bot.MARKET_PATH, 'r') as file:
            self.iventory = json.load(file)

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
        for id in self.bot.stats.get_all_users():
            money.append({
                "id": id,
                "cash": self.bot.stats.get_cash(id)})

        money.sort(key=lambda d: d["cash"], reverse=True)

        for i in range(3):
            cash = money[i]
            member = ctx.message.guild.get_member(cash["id"])

            embed.add_field(
                name=f"{i+1}. {member.display_name}",
                value=f"Cash: {cash['cash']}",
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
    if store not in self.iventory:
        embed.add_field(
            name="Invalid Store",
            value=f"{self.bot.command_prefix}market to get valid stores")
        return

    prod_dic =  find(self.iventory[store]["contents"], "name", prod)
    if prod_dic is None:
        embed.add_field(
            name="Invalid Product",
            value=f"{self.bot.command_prefix}market {store} to get valid products in this store")
        ctx.send(embed=embed)
        return

    price = prod_dic["cost"]
    if not self.bot.stats.enough_cash(ctx.message.author.id, price):
        embed.add_field(
            name="Not enough money",
            value="Item is too expensive")
        await ctx.send(embed=embed)
        return

    gear = self.bot.stats.get_gear(ctx.message.author.id)

    embed.add_field(
        name=f"{prod['simbol']}{prod_dic['name']}",
        value=f"cost: {prod_dic['cost']}\nstat: {prod_dic['stats']}")

    embed.add_field(
        name="**Replace**",
        value=f"{gear[store]['simbol']} {gear[store]['name']}\nstat: {gear[store]['stats']}")

    embed.set_footer(text="select to buy")

    self.bot.stats.spend_cash(ctx.message.author.id, price)

    msg = await ctx.send(embed=embed)
    if not await user_input_bool(self.bot, ctx.message.author, msg):
        self.bot.stats.give_cash(ctx.message.author.id, price)
        return

    try:
        self.bot.stats.set_gear(
            ctx.message.author.id,
            Gear(
                store,
                prod_dic["stats"],
                prod_dic["name"],
                prod_dic["simbol"]))

        await ctx.send("Transaction was successfull")
    except Exception as e:
        print(e)
        await ctx.send("Something unexpected went wrong")
        self.bot.stats.give_cash(ctx.message.author.id, price)

    self.bot.stats.save_stats()


async def market_stalls(self, ctx):
    embed = default_embed(self, ctx)
    for store in self.iventory.keys():
        embed.add_field(
            name=f"{self.inventory[store]['simbol']} {store}",
            value=self.iventory[store]["description"])

    embed.set_footer(text=f"{self.bot.command_prefix}market [store] to see one store")

    await ctx.send(embed=embed)

async def stall(self, ctx, store):
    embed = default_embed(self, ctx)
    store = store.lower()
    if store in self.iventory:
        store_items(
            embed,
            self.iventory[store]["stats"],
            self.iventory[store]["contents"])

        embed.set_footer(text=f"{self.bot.command_prefix}market {store} [tool] to buy from store")
    else:
        embed.add_field(
            name="Invalid Store",
            value=f"{self.bot.command_prefix}market to get valid stores")
    await ctx.send(embed=embed)

def store_items(embed, stat, items):
    items.sort(key=lambda i: i["stats"])

    for item in items:
        embed.add_field(
            name=f'{item["simbol"]}{item["name"]}',
            value=f'cost: {stat}\n{item["stats"]}: {item["cost"]}\n',
            inline=False)

def default_embed(self, ctx):
    embed = discord.Embed(
            title = f'Market de {ctx.message.guild.name}',
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
