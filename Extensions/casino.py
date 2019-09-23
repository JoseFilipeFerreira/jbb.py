import discord
from discord.ext import commands
import random
import asyncio
import time
from random import randint, choice
from aux.cash import enough_cash, spend_cash, get_cash, RepresentsInt, save_stats, hours_passed 
from PIL import Image, ImageDraw

class Casino(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setAllCash',
                      description="set money of everyones cash [OWNER ONLY]",
                      brief="set all cash")
    async def setAllCash(self, ctx, number):
        appInfo = await self.bot.application_info()
        if ctx.message.author != appInfo.owner:
            await self.bot.say("Invalid User")
            return
        if not RepresentsInt(number):
            await self.bot.say("Invalid amount")
            return

        for key in self.bot.stats:
            self.bot.stats[key]["cash"] = int(number)
        save_stats(self.bot)
    
    @commands.command(name='beg',
                      description="get one coin every 24 hours",
                      brief="beg for coins")
    async def beg(self, ctx):
        if ctx.message.channel.name not in ['nsfw']:
            await self.bot.say(
                "This command must be done in #nsfw"
            )
            return
        id = ctx.message.author.id
        if id not in self.bot.stats:
            self.bot.stats[id] = {"death": 0, "wins": 0, "kills": 0, "cash": 1, "last_beg": time.time()}
        else:
            if "last_beg" not in self.bot.stats[id]:
                self.bot.stats[id]["last_beg"] = time.time()
                get_cash(self.bot, id, 1)
                await self.bot.say("Have 1 coin.")
            
            elif hours_passed(self.bot.stats[id]["last_beg"], time.time()) > 24:
                self.bot.stats[id]["last_beg"] = time.time()
                get_cash(self.bot, id, 1)
                await self.bot.say("Have 1 coin.")
            
            else:
                await self.bot.say("No coin for you.")
        self.bot.stats[id]["bet"] = True
        save_stats(self.bot)


    @commands.command(name='roulette',
                      description="Bet on a roulette spin\n\n**red/black/green** 2x money\n**odd/even** 2x money\n**high/low** 2x money\n**number** 37x money",
                      brief="Play roulette")
    async def roulette(self, ctx, amount, bet):
        if ctx.message.channel.name not in ['nsfw']:
            await self.bot.say(
                "This command must be done in #nsfw"
            )
            return
        rOrder = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        if not RepresentsInt(amount):
            await self.bot.say("Invalid amount")
            return
        amount = int(amount)

        if amount <= 0:
            await self.bot.say("Invalid amount")
            return
        
        if not enough_cash(self.bot, ctx.message.author.id, amount):
            await self.bot.say("Not enough cash to bet")
            return
        
        bet = bet.lower()

        if bet not in ["red", "black","green", "odd", "even", "high", "low"] and (not RepresentsInt(bet)):
            await self.bot.say("Invalid bet")
            return
        
        pNumbers = []
        win = 0

        if RepresentsInt(bet):
            bet = int(bet)
            if bet < 0 or bet > 36:
                await self.bot.say("Invalid position")
                return
            pNumbers = [bet]
            win = amount * len(rOrder)
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
            pNumbers = rOrder[1::2]
            win = amount * 2
        elif bet == "black":
            pNumbers = rOrder[2::2]
            win = amount * 2
        elif bet == "green":
            pNumbers = [0]
            win = amount * len(rOrder)
        
        await self.bot.say(
            "**GAMBLE**\nBet {0} points in a roulete spin.\nWin {1} if correct.\n[yes/no]".format(amount, win))
        
        spend_cash(self.bot, ctx.message.author.id, amount)

        def guess_check(m):
            return m.content.lower() == 'yes' or m.content.lower() == 'no'
        
        answer = await self.bot.wait_for_message(
            timeout=10.0,
            author=ctx.message.author,
            check=guess_check)
            
        if answer is None:
            get_cash(self.bot, ctx.message.author.id, amount)
            return
        elif answer.content.lower() == 'no':
            get_cash(self.bot, ctx.message.author.id, amount)
            return
        
        pos = randint(0, len(rOrder) - 1)

        rImage = Image.open(self.bot.GAMES_PATH + "roulette.png")
        rImage = rImage.rotate(pos * 360 / len(rOrder))

        draw = ImageDraw.Draw(rImage)
        x = 405
        y = 130
        r = 18
        draw.ellipse((x-r, y-r, x+r, y+r), outline=(255,255,255), fill=(255,255,255))
        del draw

        rImage = rImage.rotate(randint(0, 360))

        rImage.save(self.bot.TMP_PATH + "roulette.png")

        result = " "

        if(rOrder[pos] in pNumbers):
            result = "You Won {0}🎉".format(win)
            get_cash(self.bot, ctx.message.author.id, win)
        
        else:
            result = "You lost {0} 💸".format(amount)

        await self.bot.send_file(
                ctx.message.channel,
                self.bot.TMP_PATH + "roulette.png",
                content=result)

        self.bot.stats[ctx.message.author.id]["bet"] = True
        save_stats(self.bot)

    @commands.command(name='roll',
                      description="roll a 20 faced dice\n\nIf an amount is specified gamble\nroll [amount] [number]",
                      brief="roll a dice")
    async def roll(self, ctx, * bet):
        if ctx.message.channel.name not in ['nsfw']:
            await self.bot.say(
                "This command must be done in #nsfw"
            )
            return
        if len(bet) == 0:
            await self.bot.say('You rolled a ' + str(randint(1,20)))

        elif len(bet) == 2 and RepresentsInt(bet[0]) and RepresentsInt(bet[1]):
            amount  = int(bet[0])
            number  = int(bet[1])

            if amount <= 0 or number < 1 or number > 20:
                await self.bot.say("Invalid bet")
                return

            win = amount * 20
            r_number = randint(1,20)

            #check if enough cash
            if not enough_cash(self.bot, ctx.message.author.id, amount):
                await self.bot.say("Not enough cash to bet")
                return

            await self.bot.say(
                "**GAMBLE**\nBet {0} points in the number {1} in a D20 roll.\nWin {2} if correct.\n[yes/no]".format(
                    amount, number, win))
        
            def guess_check(m):
                return m.content.lower() == 'yes' or m.content.lower() == 'no'
        
            answer = await self.bot.wait_for_message(
                timeout=10.0,
                author=ctx.message.author,
                check=guess_check)
            
            if answer is None:
                return
            elif answer.content.lower() == 'no':
                return
            
            if number == r_number:
                get_cash(self.bot, ctx.message.author.id, win)
                await self.bot.say("**GAMBLE**\nYou rolled a {0}\nYou won {1} 🎉".format(r_number, win))
            else:
                spend_cash(self.bot, ctx.message.author.id, amount)
                await self.bot.say("**GAMBLE**\nYou rolled a {0}\nYou lost {1} 💸".format(r_number, amount))

        else:
            await self.bot.say("Invalid bet")

        self.bot.stats[ctx.message.author.id]["bet"] = True
        save_stats(self.bot)
    
    @commands.command(name='slot',
                      description="play on a slot machine",
                      brief="slot machine")
    async def slot(self, ctx, amount):
        if ctx.message.channel.name not in ['nsfw']:
            await self.bot.say(
                "This command must be done in #nsfw"
            )
            return
        wheels_array = []
        for emoji in ctx.message.server.emojis:
            wheels_array.append(str(emoji))

        if not RepresentsInt(amount):
            await self.bot.say("Invalid bet")
            return

        amount = int(amount)

        if amount <= 0:
            await self.bot.say("Invalid bet")
            return
        
        if not enough_cash(self.bot, ctx.message.author.id, amount):
                await self.bot.say("Not enough cash to bet")
                return
        
        spend_cash(self.bot, ctx.message.author.id, amount)

        await self.bot.say(
                "**GAMBLE**\nBet {0} points in the slot machine.\nWin up to {1}.\n[yes/no]".format(
                    amount, amount * 30))
        
        def guess_check(m):
            return m.content.lower() == 'yes' or m.content.lower() == 'no'
        
        answer = await self.bot.wait_for_message(
            timeout=10.0,
            author=ctx.message.author,
            check=guess_check)
            
        if answer is None:
            get_cash(self.bot, ctx.message.author.id, amount)
            return
        elif answer.content.lower() == 'no':
            get_cash(self.bot, ctx.message.author.id, amount)
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
            get_cash(self.bot, ctx.message.author.id, prize)
        
        await self.bot.say(slot)
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
