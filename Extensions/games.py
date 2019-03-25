import discord
from discord.ext import commands
import random
from random import randint
from random import choice
import asyncio
from aux import enough_cash, spend_cash, get_cash, RepresentsInt


class Games():
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='flip',
                      description="flip a coin",
                      brief="flip a coin",
                      pass_context=True)
    async def flip(self, ctx):
        n = randint(0,10000)
        line = 'WTF the coin landed upright!'
        if(n<5000): line = 'You got tails'
        elif(n<10000): line = 'You got heads'
    
        await self.bot.say(line)
    
    @commands.command(name='pick',
                      description="pick a random card from a deck",
                      brief="pick a card",
                      pass_context=True)
    async def pick(self, ctx):
        simbolo = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei']
        naipe = ['paus', 'ouros', 'copas', 'espadas']
        await self.bot.say(choice(simbolo) + ' de ' + choice(naipe))
    
    
    @commands.command(name='rps',
                      description="play rock paper scissors against the bot",
                      brief="play rock paper scissors",
                      pass_context=True)
    async def rps(self, ctx, player):
        appInfo = await self.bot.application_info()
        if(player in ['rock','paper','scissors','r','p','s']):
            cpu = choice(['rock','paper','scissors'])
            player = simpRPS(player)
            result = "**" + appInfo.name + " won!**"
            if (player == cpu):
                result = "**It´s a tie!**"
            if (player == "rock" and cpu == "scissors"):
                result = "**You won!**"
            if (player == "paper" and cpu == "rock"):
                result = "**You won!**"
            if (player == "scissors" and cpu == "paper"):
                result = "**You won!**"
            await self.bot.say('You played ' + player + '\n' + appInfo.name + ' played ' + cpu + '\n' + result)
        else:
            await self.bot.say('*Invalid*')
    
    
    @commands.command(name='choose',
                      description="choose from the query",
                      brief="choose from the query",
                      pass_context=True)
    async def choose(self, ctx, *choices : str):
        """Chooses between multiple choices."""
        if all(('@' not in choice) for choice in choices):
            await self.bot.say(choice(choices))
    
    @commands.command(name='magicball',
                      description="gives answer from very likely to impossible",
                      brief="like a 8ball",
                      pass_context=True)
    async def magicball(self, ctx):
        a = ['Most likely', 'Very doubtful', 'Ask again', 'As I see it, yes', 'My sources say no', 'Cannot perdict now', 'Yes', 'Dont count on it', 'Without a doubt', 'Better not tell you']
        await self.bot.say(choice(a))
 
    @commands.command(name='guess',
                      description="guess the coin the bot is thinking about",
                      brief="guess coin",
                      pass_context=True)
    async def guess(self, ctx):
        await self.bot.say("Guess how the coin landed (head/tail)")
        
        def guess_check(m):
            return m.content.lower() == 'tail' or m.content.lower() == 'head'
        
        await self.bot.send_typing(ctx.message.channel)
        guess = await self.bot.wait_for_message(
            timeout=10.0,
            author=ctx.message.author,
            check=guess_check)

        n = randint(0,1)
        answer  = 'tail'
        if(n==1): answer = 'head'

        if guess is None:
            await self.bot.say('You took too long. I got {}'.format(answer))
        elif guess.content == answer:
            await self.bot.say('You guessed it!')
        else:
            await self.bot.say("You're wrong. I got {}".format(answer))

    @commands.command(name='vote',
                      description="creates a poll with given query or default text",
                      brief="create a poll",
                      aliases=['poll'],
                      pass_context=True)
    async def vote(self, ctx, *quote):
    #create poll
        if not quote:
           quote = 'Vote here'
        else:
           quote = ' '.join(word for word in quote)
        await self.bot.delete_message(ctx.message)
        vote = await self.bot.say('**{0}** (poll by {1})'.format(quote, ctx.message.author.mention))
        await self.bot.add_reaction(vote, '\U0000274C')
        await self.bot.add_reaction(vote, '\U00002705')

def getRPS():
    n = randint(0,2)
    if(n == 0):
        return "rock"
    if(n == 1):
        return "paper"
    return "scissors"


def simpRPS(hand):
    if (hand == "r"):
        hand = "rock"
    if (hand == "p"):
        hand = "paper"
    if (hand == "s"):
        hand = "scissors"
    return hand
    

def setup(bot):
    bot.add_cog(Games(bot))
