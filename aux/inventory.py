import discord
import time

def get_empty_inventory():
    inv = {}
    inv["gear"] = {
            "armor": get_empty_gear_object(),
            "weapon": get_empty_gear_object(),
            "shield": get_empty_gear_object()}
    return inv

def get_empty_gear_object():
    simb = {}
    simb["simbol"] = ":heavy_multiplication_x:"
    simb["stats"]  = 0
    simb["name"] = "default"
    return simb

def normalize_inventory(bot, id):
    if id not in bot.stats:
        bot.stats[id] = get_empty_stats()
    if "inventory" not in bot.stats[id]:
        bot.stats[id]["inventory"] = get_empty_inventory()

    if "gear" not in bot.stats[id]["inventory"]:
        bot.stats[id]["inventory"]["gear"] = {
            "armor": get_empty_gear_object(),
            "weapon": get_empty_gear_object(),
            "shield": get_empty_gear_object()}
    if "armor" not in bot.stats[id]["inventory"]["gear"]:
        bot.stats[id]["inventory"]["gear"]["armor"] = get_empty_gear_object()    
    if "weapon" not in bot.stats[id]["inventory"]["gear"]:
        bot.stats[id]["inventory"]["gear"]["weapon"] = get_empty_gear_object()    
    if "shield" not in bot.stats[id]["inventory"]["gear"]:
        bot.stats[id]["inventory"]["gear"]["shield"] = get_empty_gear_object()
    for item in bot.stats[id]["inventory"]["gear"]:
        if "simbol" not in bot.stats[id]["inventory"]["gear"][item]:
            bot.stats[id]["inventory"]["gear"][item]["simbol"] = ":heavy_multiplication_x:"
        if "stats" not in bot.stats[id]["inventory"]["gear"][item]:
            bot.stats[id]["inventory"]["gear"][item]["stats"] = 0
        if "name" not in bot.stats[id]["inventory"]["gear"][item]:
            bot.stats[id]["inventory"]["gear"][item]["name"] = "default"

def normalize_stat(bot, id):
    if id not in bot.stats:
        bot.stats[id] = get_empty_stats()
    
    if "death" not in bot.stats[id]:
        bot.stats[id]["death"] = 0 
    if "wins" not in bot.stats[id]:
        bot.stats[id]["wins"] = 0
    if "kills" not in bot.stats[id]:
        bot.stats[id]["kills"] = 0
    if "cash" not in bot.stats[id]:
        bot.stats[id]["cash"] = 10
    if "last_beg" not in bot.stats[id]:
        bot.stats[id]["last_beg"] = time.time()
    if "bet" not in bot.stats[id]:
        bot.stats[id]["bet"] = False
    normalize_inventory(bot, id)

def get_empty_stats():
    stat = {}
    stat["death"] = 0
    stat["wins"] = 0
    stat["kills"] = 0
    stat["cash"] = 10
    stat["last_beg"] = time.time()
    stat["inventory"] = get_empty_inventory()
    stat["bet"] = False
    
def update_kills(bot, id, death, kills, wins):
    normalize_stat(bot, id)
    bot.stats[id]["kills"] += kills
    bot.stats[id]["death"] += death
    bot.stats[id]["wins"]  += wins

def get_inventory(bot, id):
    normalize_stat(bot, id)
    return bot.stats[id]["inventory"]

def get_embed_inventory(bot, id, name):
    inv = get_inventory(bot, id)
    embed = discord.Embed(
            title = "Inventory of {}".format(name),
            color=bot.embed_color)
    embed.set_thumbnail(
            url="https://cdn4.iconfinder.com/data/icons/video-game-items-concepts/128/inventory-bag-2-512.png")
    
    embed.add_field(
            name="⚔ weapon",
            value="{1} {2}\ndamage: {0}".format(
                inv["gear"]["weapon"]["stats"],
                inv["gear"]["weapon"]["simbol"],
                inv["gear"]["weapon"]["name"]) 
            )

    embed.add_field(
            name="⚓armor",
            value="{1} {2}\nprotection: {0}".format(
                inv["gear"]["armor"]["stats"],
                inv["gear"]["armor"]["simbol"],
                inv["gear"]["armor"]["name"]) 
            )

    embed.add_field(
            name="🛡 shield",
            value="{1} {2}\nblock: {0}".format(
                inv["gear"]["shield"]["stats"],
                inv["gear"]["shield"]["simbol"],
                inv["gear"]["shield"]["name"]) 
            )

    embed.add_field(
                name="💰Cash",
                value=bot.stats[id]["cash"])

    embed.set_footer(text = "Inventory")

    return embed

