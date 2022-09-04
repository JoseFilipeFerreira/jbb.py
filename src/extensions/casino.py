import time
from random import randint
import discord
from discord.ext import commands
from PIL import Image, ImageDraw
from aux.misc import represents_int, hours_passed
from aux.message import user_input_bool

class Casino(commands.Cog):
    """Bet all your life savings here"""
    def __init__(self, bot):
        self.bot = bot
        self.r_order = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

    @commands.command(name='beg',
                      description="get one coin every 24 hours... or more?",
                      brief="beg for coins")
    @commands.is_nsfw()
    async def beg(self, ctx):
        id = ctx.message.author.id
        if hours_passed(self.bot.stats.get_last_beg(id), time.time()) > 24:
            self.bot.stats.set_last_beg(id, time.time())

            if randint(0, 100) == 1:
                await ctx.send("Feeling a bit generous today. Have 100 coins.")
                self.bot.stats.give_cash(id, 100)
            else:
                await ctx.send("Have 1 coin.")
                self.bot.stats.give_cash(id, 1)

        else:
            await ctx.send("No coin for you.")

        self.bot.stats.set_bet(id, True)
        self.bot.stats.save_stats()

    @commands.command(name='roulette',
                      brief="Play roulette")
    @commands.is_nsfw()
    async def roulette(self, ctx, amount : int, bet):
        """Bet on a roulette spin

        **red/black/green** 2x money
        **odd/even** 2x money
        **high/low** 2x money
        **number** 37x money"""
        bet = bet.lower()

        if amount <= 0:
            await ctx.send("Invalid amount")
            return

        if not self.bot.stats.enough_cash(ctx.message.author.id, amount):
            await ctx.send("Not enough cash to bet")
            return

        if bet not in ["red", "black","green", "odd", "even", "high", "low"] and (not represents_int(bet)):
            await ctx.send("Invalid bet")
            return

        p_numbers = []
        win = 0

        if represents_int(bet):
            bet = int(bet)
            if bet < 0 or bet > 36:
                await ctx.send("Invalid position")
                return
            p_numbers = [bet]
            win = amount * len(self.r_order)
        elif bet == "odd":
            p_numbers = list(range(1, 37, 2))
            win = amount * 2
        elif bet == "even":
            p_numbers = list(range(2, 36, 2))
            win = amount * 2
        elif bet == "low":
            p_numbers = list(range(1, 19))
            win = amount * 2
        elif bet == "high":
            p_numbers = list(range(19, 36))
            win = amount * 2
        elif bet == "red":
            p_numbers = self.r_order[1::2]
            win = amount * 2
        elif bet == "black":
            p_numbers = self.r_order[2::2]
            win = amount * 2
        elif bet == "green":
            p_numbers = [0]
            win = amount * len(self.r_order)

        msg = await ctx.send(
            f"**GAMBLE**\nBet {amount} points in a roulete spin.\nWin {win} if correct.")

        self.bot.stats.spend_cash(ctx.message.author.id, amount)

        if not await user_input_bool(self.bot, ctx.message.author, msg):
            self.bot.stats.give_cash(ctx.message.author.id, amount)
            return

        pos = randint(0, len(self.r_order) - 1)

        r_image = Image.open(self.bot.GAMES_PATH + "roulette.png")
        r_image = r_image.rotate(pos * 360 / len(self.r_order))

        draw = ImageDraw.Draw(r_image)
        ball_x = 405
        ball_y = 130
        ball_r = 18
        draw.ellipse((ball_x-ball_r, ball_y-ball_r, ball_x+ball_r, ball_y+ball_r), outline=(255,255,255), fill=(255,255,255))
        del draw

        r_image = r_image.rotate(randint(0, 360))

        r_image.save(self.bot.TMP_PATH + "roulette.png")

        result = " "

        if self.r_order[pos] in p_numbers:
            result = f"You Won {win}🎉"
            self.bot.stats.give_cash(ctx.message.author.id, win)
        else:
            result = f"You lost {amount} 💸"

        await ctx.send(
                result,
                file=discord.File(
                    self.bot.TMP_PATH + "roulette.png"))

        self.bot.stats.set_bet(ctx.message.author.id, True)
        self.bot.stats.save_stats()

    @commands.command(name='roll',
                      brief="roll a dice")
    @commands.is_nsfw()
    async def roll(self, ctx, amount : int = None, number : int = None):
        """roll a 20 faced dice
        If an amount is specified gamble"""
        if amount is None and number is None:
            await ctx.send('You rolled a ' + str(randint(1,20)))

        elif number is not None and number is not None:
            if amount <= 0 or number < 1 or number > 20:
                await ctx.send("Invalid bet")
                return

            win = amount * 20
            r_number = randint(1,20)

            #check if enough cash
            if not self.bot.stats.enough_cash(ctx.message.author.id, amount):
                await ctx.send("Not enough cash to bet")
                return

            msg = await ctx.send(
                f"**GAMBLE**\nBet {amount} points in the number {number} in a D20 roll.\nWin {win} if correct.")

            self.bot.stats.spend_cash(ctx.message.author.id, amount)

            if not await user_input_bool(self.bot, ctx.message.author, msg):
                self.bot.stats.give_cash(ctx.message.author.id, amount)
                return

            if number == r_number:
                self.bot.stats.give_cash(ctx.message.author.id, win)
                await ctx.send(f"**GAMBLE**\nYou rolled a {r_number}\nYou won {win} 🎉")
            else:
                await ctx.send(f"**GAMBLE**\nYou rolled a {r_number}\nYou lost {amount} 💸")
        else:
            await ctx.send("Invalid bet")

        self.bot.stats.set_bet(ctx.message.author.id, True)
        self.bot.stats.save_stats()

    @commands.command(name='slot',
                      description="play on a slot machine",
                      brief="slot machine")
    @commands.is_nsfw()
    async def slot(self, ctx, amount:int):
        wheels_array = []
        for emoji in ctx.message.guild.emojis:
            wheels_array.append(str(emoji))

        if amount <= 0:
            await ctx.send("Invalid bet")
            return

        if not self.bot.stats.enough_cash(ctx.message.author.id, amount):
            await ctx.send("Not enough cash to bet")
            return

        msg = await ctx.send(
            "**GAMBLE**\nBet {amount} points in the slot machine.\nWin up to {amount * 30}.")

        self.bot.stats.spend_cash(ctx.message.author.id, amount)

        if not await user_input_bool(self.bot, ctx.message.author, msg):
            self.bot.stats.give_cash(ctx.message.author.id, amount)
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
            slot += f"You lost {amount} 💸"
        else:
            slot += f"You won {prize} 🎉"
            self.bot.stats.give_cash(ctx.message.author.id, prize)

        await ctx.send(slot)
        self.bot.stats.set_bet(ctx.message.author.id, True)
        self.bot.stats.save_stats()

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
