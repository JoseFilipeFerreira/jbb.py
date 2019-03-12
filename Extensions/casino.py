import discord
from discord.ext import commands
import random
from random import randint
from random import choice
import asyncio
from aux import enough_cash, spend_cash, get_cash, RepresentsInt, save_stats 


class Casino():
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setAllCash',
                      description="set money of everyones cash [OWNER ONLY]",
                      brief="set all cash",
                      pass_context=True)
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

    @commands.command(name='roll',
                      description="roll a 20 faced dice\n\nIf an amount is specified gamble\nroll [amount] [number]",
                      brief="roll a dice",
                      pass_context=True)
    async def roll(self, ctx, * bet):
        if len(bet) == 0:
            await self.bot.say('You rolled a ' + str(randint(1,20)))

        elif len(bet) == 2 and RepresentsInt(bet[0]) and RepresentsInt(bet[1]):
            amount  = int(bet[0])
            number  = int(bet[1])

            if amount <= 0 or number < 1 or number > 20:
                await self.bot.say("Invalid bet")
                return

            win = amount * 10
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
        
        save_stats(self.bot)
    
    @commands.command(name='slot',
                      description="play on a slot machine",
                      brief="slot machine",
                      pass_context=True)
    async def slot(self, ctx, amount):
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

        await self.bot.say(
                "**GAMBLE**\nBet {0} points in the slot machine.\nWin up to {1}.\n[yes/no]".format(
                    amount, amount * 80))
        
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
        
        w1 = randint(0, len(wheels_array) - 1)
        w2 = randint(0, len(wheels_array) - 1)
        w3 = randint(0, len(wheels_array) - 1)

        slot = "**YOU LOST**\n"
        prize = 0

        if (w1 - w2) == (w2 - w3):
            prize = amount * 80
            slot = "**YOU WON**\n"
        
        elif (w1 - w2) == 0 or (w2 - w3) == 0 or (w1 - w3) == 0:
            prize = amount * 10
            slot = "**YOU WON**\n"

        elif bool(abs(w1 - w2) == 1) != bool(abs(w2 - w3) == 1):
            prize = amount * 5
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
            spend_cash(self.bot, ctx.message.author.id, amount)
        else:
            slot += "You won {0} 🎉".format(prize)
            get_cash(self.bot, ctx.message.author.id, prize)
        
        await self.bot.say(slot)

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
