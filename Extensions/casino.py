import discord
from discord.ext import commands
import random
import asyncio
import time
from random import randint, choice
from aux.cash import enough_cash, spend_cash, give_cash, RepresentsInt, save_stats, hours_passed 
from aux.inventory import get_stat
from PIL import Image, ImageDraw

class Casino(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.rOrder = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

    @commands.command(name='beg',
                      description="get one coin every 24 hours",
                      brief="beg for coins")
    @commands.is_nsfw()
    async def beg(self, ctx):
        id = ctx.message.author.id
        stat = get_stat(self.bot, id)
        if hours_passed(stat["last_beg"], time.time()) > 24:
            stat["last_beg"] = time.time()
            give_cash(self.bot, id, 1)
            await ctx.send("Have 1 coin.")
        else:
            await ctx.send("No coin for you.")
        stat["bet"] = True
        save_stats(self.bot)

    @commands.command(name='roulette',
                      description="Bet on a roulette spin\n\n**red/black/green** 2x money\n**odd/even** 2x money\n**high/low** 2x money\n**number** 37x money",
                      brief="Play roulette")
    @commands.is_nsfw()
    async def roulette(self, ctx, amount, bet):
        bet = bet.lower()
        if not RepresentsInt(amount):
            await ctx.send("Invalid amount")
            return
        amount = int(amount)

        if amount <= 0:
            await ctx.send("Invalid amount")
            return
        
        if not enough_cash(self.bot, ctx.message.author.id, amount):
            await ctx.send("Not enough cash to bet")
            return
        

        if bet not in ["red", "black","green", "odd", "even", "high", "low"] and (not RepresentsInt(bet)):
            await ctx.send("Invalid bet")
            return
        
        pNumbers = []
        win = 0

        if RepresentsInt(bet):
            bet = int(bet)
            if bet < 0 or bet > 36:
                await ctx.send("Invalid position")
                return
            pNumbers = [bet]
            win = amount * len(self.rOrder)
        elif bet == "odd":
            pNumbers = list(range(1, 36, 2))
            win = amount * 2
        elif bet == "even":
            pNumbers = list(range(2, 36, 2))
            win = amount * 2
        elif bet == "low":
            pNumbers = list(range(1, 18))
            win = amount * 2
        elif bet == "high":
            pNumbers = list(range(19, 36))
            win = amount * 2
        elif bet == "red":
            pNumbers = self.rOrder[1::2]
            win = amount * 2
        elif bet == "black":
            pNumbers = self.rOrder[2::2]
            win = amount * 2
        elif bet == "green":
            pNumbers = [0]
            win = amount * len(self.rOrder)
        
        msg = await ctx.send(
            "**GAMBLE**\nBet {0} points in a roulete spin.\nWin {1} if correct.".format(amount, win))
       
        await msg.add_reaction('\U0000274C')
        await msg.add_reaction('\U00002705')
    
        spend_cash(self.bot, ctx.message.author.id, amount)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['\U00002705', '\U0000274C']  
    
        try:
             reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            give_cash(self.bot, ctx.message.author.id, amount)
            return

        await msg.clear_reactions()

        if reaction.emoji ==  '\U0000274C':
            give_cash(self.bot, ctx.message.author.id, amount)
            return
        
        pos = randint(0, len(self.rOrder) - 1)

        rImage = Image.open(self.bot.GAMES_PATH + "roulette.png")
        rImage = rImage.rotate(pos * 360 / len(self.rOrder))

        draw = ImageDraw.Draw(rImage)
        x = 405
        y = 130
        r = 18
        draw.ellipse((x-r, y-r, x+r, y+r), outline=(255,255,255), fill=(255,255,255))
        del draw

        rImage = rImage.rotate(randint(0, 360))

        rImage.save(self.bot.TMP_PATH + "roulette.png")

        result = " "

        if(self.rOrder[pos] in pNumbers):
            result = "You Won {0}🎉".format(win)
            give_cash(self.bot, ctx.message.author.id, win)
        
        else:
            result = "You lost {0} 💸".format(amount)

        await ctx.send(
                result,
                file=discord.File(
                    self.bot.TMP_PATH + "roulette.png"))

        self.bot.stats[ctx.message.author.id]["bet"] = True
        save_stats(self.bot)

    @commands.command(name='roll',
                      description="roll a 20 faced dice\n\nIf an amount is specified gamble\nroll [amount] [number]",
                      brief="roll a dice")
    @commands.is_nsfw()
    async def roll(self, ctx,* bet):
        if len(bet) == 0:
            await ctx.send('You rolled a ' + str(randint(1,20)))

        elif len(bet) == 2 and RepresentsInt(bet[0]) and RepresentsInt(bet[1]):
            amount  = int(bet[0])
            number  = int(bet[1])

            if amount <= 0 or number < 1 or number > 20:
                await ctx.send("Invalid bet")
                return

            win = amount * 20
            r_number = randint(1,20)

            #check if enough cash
            if not enough_cash(self.bot, ctx.message.author.id, amount):
                await ctx.send("Not enough cash to bet")
                return

            msg = await ctx.send(
                "**GAMBLE**\nBet {0} points in the number {1} in a D20 roll.\nWin {2} if correct.".format(
                    amount, number, win))
        
            await msg.add_reaction('\U0000274C')
            await msg.add_reaction('\U00002705')
    
            spend_cash(self.bot, ctx.message.author.id, amount)

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['\U00002705', '\U0000274C']  
    
            try:
                 reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                give_cash(self.bot, ctx.message.author.id, amount)
                return

            await msg.clear_reactions()

            if reaction.emoji ==  '\U0000274C':
                give_cash(self.bot, ctx.message.author.id, amount)
                return
        
            if number == r_number:
                give_cash(self.bot, ctx.message.author.id, win)
                await ctx.send("**GAMBLE**\nYou rolled a {0}\nYou won {1} 🎉".format(r_number, win))
            else:
                spend_cash(self.bot, ctx.message.author.id, amount)
                await ctx.send("**GAMBLE**\nYou rolled a {0}\nYou lost {1} 💸".format(r_number, amount))

        else:
            await ctx.send("Invalid bet")

        self.bot.stats[ctx.message.author.id]["bet"] = True
        save_stats(self.bot)
    
    @commands.command(name='slot',
                      description="play on a slot machine",
                      brief="slot machine")
    @commands.is_nsfw()
    async def slot(self, ctx, amount):
        wheels_array = []
        for emoji in ctx.message.guild.emojis:
            wheels_array.append(str(emoji))

        if not RepresentsInt(amount):
            await ctx.send("Invalid bet")
            return

        amount = int(amount)

        if amount <= 0:
            await ctx.send("Invalid bet")
            return
        
        if not enough_cash(self.bot, ctx.message.author.id, amount):
                await ctx.send("Not enough cash to bet")
                return
        
        msg = await ctx.send(
                "**GAMBLE**\nBet {0} points in the slot machine.\nWin up to {1}.".format(
                    amount, amount * 30))

        await msg.add_reaction('\U0000274C')
        await msg.add_reaction('\U00002705')
    
        spend_cash(self.bot, ctx.message.author.id, amount)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['\U00002705', '\U0000274C']  
    
        try:
             reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            give_cash(self.bot, ctx.message.author.id, amount)
            return

        await msg.clear_reactions()

        if reaction.emoji ==  '\U0000274C':
            give_cash(self.bot, ctx.message.author.id, amount)
            return

        w1 = randint(0, len(wheels_array) - 1)
        w2 = randint(0, len(wheels_array) - 1)
        w3 = randint(0, len(wheels_array) - 1)

        slot = "**YOU LOST**\n"
        prize = 0

        if (w1 - w2) == (w2 - w3) and (w1 - w2) in [-1,0,1]:
            prize = amount * 30
            slot = "**YOU WON**\n"
        
        elif (w1 - w2) == 0 or (w2 - w3) == 0 or (w1 - w3) == 0:
            prize = amount * 10
            slot = "**YOU WON**\n"

        slot += " {0} | {1} | {2}\n".format(
            get_prev_slot(wheels_array, w1),
            get_prev_slot(wheels_array, w2),
            get_prev_slot(wheels_array, w3)
        )
        slot += "------------------\n"
        slot += " {0} | {1} | {2}\n".format(
            wheels_array[w1],
            wheels_array[w2],
            wheels_array[w3])
        
        slot += "------------------\n"
        slot += " {0} | {1} | {2}\n\n".format(
            get_next_slot(wheels_array, w1),
            get_next_slot(wheels_array, w2),
            get_next_slot(wheels_array, w3)
        )

        if prize == 0:
            slot += "You lost {0} 💸".format(amount)
        else:
            slot += "You won {0} 🎉".format(prize)
            give_cash(self.bot, ctx.message.author.id, prize)
        
        await ctx.send(slot)
        self.bot.stats[id]["bet"] = True
        save_stats(self.bot)

def get_prev_slot(arr, pos):
    npos = pos - 1
    if npos < 0:
        npos = len(arr) - 1
    return arr[npos]

def get_next_slot(arr, pos):
    npos = pos + 1
    if npos > len(arr) - 1:
        npos = 0
    return arr[npos]

def setup(bot):
    bot.add_cog(Casino(bot))
