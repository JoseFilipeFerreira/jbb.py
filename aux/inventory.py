import discord
import time

def get_empty_stats():
    stat = {}
    stat["death"] = 0
    stat["wins"] = 0
    stat["kills"] = 0
    stat["cash"] = 10
    stat["last_beg"] = time.time()
    stat["inventory"] = {
            "gear": {
                "shield": {
                    "stats": 1,
                    "name": "glasses",
                    "simbol": "👓"},
                "weapon": {
                    "stats": 1,
                    "name": "fists",
                    "simbol": "🤜"},
                "armor": {
                    "stats": 1,
                    "name": "Skin",
                    "simbol": "👤"}}}
    stat["bet"] = False
    return stat

def update_kills(bot, id, death, kills, wins):
    if id not in bot.stats:
        bot.stats[id] = get_empty_stats()
    bot.stats[id]["kills"] += kills
    bot.stats[id]["death"] += death
    bot.stats[id]["wins"]  += wins

def get_stat(bot, id):
    if id not in bot.stats:
        bot.stats[id] = get_empty_stats()
    return bot.stats[id]

def get_inventory(bot, id):
    if id not in bot.stats:
        bot.stats[id] = get_empty_stats()
    return bot.stats[id]["inventory"]

def get_embed_inventory(bot, id, name, embed_colour):
    inv = get_inventory(bot, id)
    embed = discord.Embed(
            title = f"Inventory of {name}",
            color=embed_colour)
    embed.set_thumbnail(
            url="https://cdn4.iconfinder.com/data/icons/video-game-items-concepts/128/inventory-bag-2-512.png")

    embed.add_field(
        name="⚔ weapon",
        value="{1} {2}\ndamage: {0}".format(
            inv["gear"]["weapon"]["stats"],
            inv["gear"]["weapon"]["simbol"],
            inv["gear"]["weapon"]["name"]))

    embed.add_field(
        name="⚓armor",
        value="{1} {2}\nprotection: {0}".format(
            inv["gear"]["armor"]["stats"],
            inv["gear"]["armor"]["simbol"],
            inv["gear"]["armor"]["name"]))

    embed.add_field(
        name="🛡 shield",
        value="{1} {2}\nblock: {0}".format(
            inv["gear"]["shield"]["stats"],
            inv["gear"]["shield"]["simbol"],
            inv["gear"]["shield"]["name"]))

    embed.add_field(
        name="💰Cash",
        value=bot.stats[id]["cash"])

    embed.set_footer(text = "Inventory")

    return embed

