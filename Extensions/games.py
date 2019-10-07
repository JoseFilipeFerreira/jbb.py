import discord
from discord.ext import commands
import random
from random import randint
from random import choice
import asyncio

class Games(commands.Cog):
    """Play games with your friends"""    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='flip',
                      description="flip a coin",
                      brief="flip a coin")
    async def flip(self, ctx):
        n = randint(0,10000)
        line = 'WTF the coin landed upright!'
        if(n<5000): line = 'You got tails'
        elif(n<10000): line = 'You got heads'
    
        await ctx.send(line)
    
    @commands.command(name='pick',
                      description="pick a random card from a deck",
                      brief="pick a card")
    async def pick(self, ctx):
        simbolo = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei']
        naipe = ['paus', 'ouros', 'copas', 'espadas']
        await ctx.send(choice(simbolo) + ' de ' + choice(naipe))
    
    
    @commands.command(name='rps',
                      description="play rock paper scissors against the bot",
                      brief="play rock paper scissors")
    async def rps(self, ctx, player):
        appInfo = await self.bot.application_info()
        if(player in ['rock','paper','scissors','r','p','s']):
            cpu = choice(['rock','paper','scissors'])
            player = simpRPS(player)
            result = "**" + appInfo.name + " won!**"
            if (player == cpu):
                result = "**It´s a tie!**"
            elif (player == "rock" and cpu == "scissors"):
                result = "**You won!**"
            elif (player == "paper" and cpu == "rock"):
                result = "**You won!**"
            elif (player == "scissors" and cpu == "paper"):
                result = "**You won!**"
            await ctx.send('You played ' + player + '\n' + appInfo.name + ' played ' + cpu + '\n' + result)
        else:
            await ctx.send('*Invalid*')
    
    
    @commands.command(name='choose',
                      description="choose from the query",
                      brief="choose from the query")
    async def choose(self, ctx, *choices : str):
        if all(('@' not in choice) for choice in choices):
            await ctx.send(choice(choices))
    
    @commands.command(name='magicball',
                      description="gives answer from very likely to impossible",
                      brief="like a 8ball")
    async def magicball(self, ctx):
        a = ['Most likely', 'Very doubtful', 'Ask again', 'As I see it, yes', 'My sources say no', 'Cannot perdict now', 'Yes', 'Dont count on it', 'Without a doubt', 'Better not tell you']
        await ctx.send(choice(a))
 
    @commands.command(name='guess',
                      description="guess the coin the bot is thinking about",
                      brief="guess coin")
    async def guess(self, ctx):
        await ctx.send("Guess how the coin landed (head/tail)")
        
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
            await ctx.send(f'You took too long. I got {answer}')
        elif guess.content == answer:
            await ctx.send('You guessed it!')
        else:
            await ctx.send(f"You're wrong. I got {answer}")

    @commands.command(name='vote',
                      description="creates a poll with given query or default text",
                      brief="create a poll",
                      aliases=['poll'])
    async def vote(self, ctx, *, quote = None):
        if not quote:
           quote = 'Vote here'
        await ctx.message.delete()
        vote = await ctx.send('**{0}**\n(poll by {1})'.format(quote, ctx.message.author.mention))
        await vote.add_reaction('\U0000274C')
        await vote.add_reaction('\U00002705')

def getRPS():
    n = randint(0,2)
    if(n == 0):
        return "rock"
    elif(n == 1):
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
