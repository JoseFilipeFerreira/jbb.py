import discord
from discord.ext import commands
import random
from random import randint
from random import choice
import asyncio
from aux import enough_cash, spend_cash, get_cash, RepresentsInt


class Casino():
    
    def __init__(self, bot):
        self.bot = bot

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
            win = amount * 10
            r_number = randint(1,20)

            #check if enough cash
            if not enough_cash(self.bot, ctx.message.author.id, amount):
                await self.bot.say("Not enough cash to bet")
                return

            await self.bot.say(
                "**GAMBLE**\nBet {0} points in the number {1} in a D20 roll.\nWin {2} if correct.".format(
                    amount, number, win))
        
            def guess_check(m):
                return m.content.lower() == 'yes' or m.content.lower() == 'no'
        
            answer = await self.bot.wait_for_message(
                timeout=10.0,
                author=ctx.message.author,
                check=guess_check)
            
            if answer.content.lower() == 'no':
                return
            
            if bet == r_number:
                get_cash(self.bot, ctx.message.author.id, win)
                await self.bot.say("**GAMBLE**\nYou rolled a {0}\nYou won {1}".format(r_number, win))
            else:
                spend_cash(self.bot, ctx.message.author.id, amount)
                await self.bot.say("**GAMBLE**\nYou rolled a {0}\nYou lost {1}".format(r_number, amount))

        else:
            await self.bot.say("Invalid bet")
    

def setup(bot):
    bot.add_cog(Casino(bot))
