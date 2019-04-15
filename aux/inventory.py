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
    if "inventory" not in bot.stats[id]:
        normalize_inventory(bot, id)

def get_empty_stats():
    stat = {}
    stat["death"] = 0
    stat["wins"] = 0
    stat["kills"] = 0
    stat["cash"] = 10
    stat["last_beg"] = time.time()
    stat["inventory"] = get_empty_inventory()
    
def update_kills(bot, id, death, kills, wins):
    if id not in bot.stats:
        bot.stats[id] = get_empty_stats()
    bot.stats[id]["kills"] += kills
    bot.stats[id]["death"] += death
    bot.stats[id]["wins"]  += wins

def get_inventory(bot, id):
    if id not in bot.stats:
        bot.stats[id] = get_empty_stats()
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
            value="damage {0} -> {1}".format(
                inv["gear"]["weapon"]["stats"],
                inv["gear"]["weapon"]["simbol"]) 
            )

    embed.add_field(
            name="⚓armor",
            value="protection {0} -> {1}".format(
                inv["gear"]["armor"]["stats"],
                inv["gear"]["armor"]["simbol"]) 
            )

    embed.add_field(
            name="🛡 shield",
            value="block {0} -> {1}".format(
                inv["gear"]["shield"]["stats"],
                inv["gear"]["shield"]["simbol"]) 
            )

    embed.add_field(
                name="💰Cash",
                value=bot.stats[id]["cash"])

    embed.set_footer(text = "Inventory")

    return embed

