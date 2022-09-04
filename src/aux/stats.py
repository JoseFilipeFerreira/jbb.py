import time
import json
import discord
from aux.misc import hours_passed

class Gear:
    def __init__(self, kind, stats, name, simbol):
        self.kind = kind
        self.stats = stats
        self.name = name
        self.simbol = simbol

    def get_kind(self):
        return self.kind

    def to_dict(self):
        return {
            "stats": self.stats,
            "name": self.name,
            "simbol": self.simbol}

class Stats:
    def __init__(self, directory):
        self.PATH = directory
        with open(self.PATH, 'r') as file:
            j = json.load(file)
            #Keys convert to string when writing to json
            self.stats = {int(key): value for key, value in j["stats"].items()}
            self.last_giveaway = j["last_giveaway"]

    def get_stat(self, user_id):
        if user_id not in self.stats:
            self.stats[user_id] = get_empty_stats()
        return self.stats[user_id]

    def get_all_users(self):
        return self.stats.keys()

    def add_user(self, user_id):
        self.stats[user_id] = get_empty_stats()

    def remove_user(self, user_id):
        self.stats.pop(user_id, None)

    def update_kills(self, user_id, death, kills, wins):
        stat = self.get_stat(user_id)
        stat["kills"] += kills
        stat["death"] += death
        stat["wins"]  += wins

    def get_inventory(self, user_id):
        return self.get_stat(user_id)["inventory"]

    def get_gear(self, user_id):
        return self.get_inventory(user_id)["gear"]

    def set_gear(self, user_id, gear):
        inv = self.get_inventory(user_id)
        if gear.get_type() in inv["gear"]:
            inv["gear"][gear.get_type()] = gear.to_dict()

    def get_cash(self, user_id):
        return self.get_stat(user_id)["cash"]

    def enough_cash(self, user_id, amount):
        return self.get_cash(user_id) >= amount

    def spend_cash(self, user_id, amount):
        if self.enough_cash(user_id, amount):
            self.give_cash(user_id, (-1) * amount)
            return True
        return False

    def give_cash(self, user_id, amount):
        self.get_stat(user_id)["cash"] += amount

    def get_bet(self, user_id):
        return self.get_stat(user_id)["bet"]

    def set_bet(self, user_id, bet):
        self.get_stat(user_id)["bet"] = bet

    def get_kdr(self, user_id):
        stat = self.get_stat(user_id)
        return stat["kills"], stat["death"]

    def get_last_beg(self, user_id):
        return self.get_stat(user_id)["last_beg"]

    def set_last_beg(self, user_id, beg_time):
        self.get_stat(user_id)["last_beg"] = beg_time

    def daily_giveaway(self, amount):
        if hours_passed(self.last_giveaway, time.time()) > 24:
            self.last_giveaway += 24*60*60
            given = 0
            for user_id in self.get_all_users():
                if self.get_bet(user_id):
                    self.give_cash(user_id, amount)
                    given += 1
            self.save_stats()
            return given
        return None

    def get_embed_inventory(self, user_id, name, embed_colour):
        inv = self.get_inventory(user_id)
        embed = discord.Embed(
                title = f"Inventory of {name}",
                color=embed_colour)
        embed.set_thumbnail(
            url="https://cdn4.iconfinder.com/data/icons/video-game-items-concepts/128/inventory-bag-2-512.png")

        embed.add_field(
            name="⚔ weapon",
            value=f'{inv["gear"]["weapon"]["stats"]} {inv["gear"]["weapon"]["simbol"]}\nblock: {inv["gear"]["weapon"]["name"]}')

        embed.add_field(
            name="⚓armor",
            value=f'{inv["gear"]["armor"]["stats"]} {inv["gear"]["armor"]["simbol"]}\nblock: {inv["gear"]["armor"]["name"]}')

        embed.add_field(
            name="🛡shield",
            value=f'{inv["gear"]["shield"]["stats"]} {inv["gear"]["shield"]["simbol"]}\nblock: {inv["gear"]["shield"]["name"]}')

        embed.add_field(
            name="💰Cash",
            value=self.get_cash(user_id))

        embed.set_footer(text = "Inventory")

        return embed

    def save_stats(self):
    #save server stats
        with open(self.PATH, 'w') as file:
            json.dump(
                {"last_giveaway":self.last_giveaway, "stats": self.stats}
               , file, indent=4)


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
