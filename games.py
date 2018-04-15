import discord
from discord.ext import commands
from random import randint

#atirar um dado com 20 faces
@bot.command(pass_context=True)
async def roll(ctx):
    await bot.say('You rolled a ' + str(randint(1,20)))


#atirar moeda ao ar (com easteregg)
@bot.command(pass_context=True)
async def flip(ctx):
    n = randint(0,10000)
    line = 'WTF the coin landed upright!'
    if(n<5000): line = 'You got tails'
    elif(n<10000): line = 'You got heads'

    await bot.say(line)


#escolher uma carta
@bot.command(pass_context=True)
async def pick(ctx):
    simbolo = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei']
    naipe = ['paus', 'ouros', 'copas', 'espadas']
    await bot.say(simbolo[randint(0,12)] + ' de ' + naipe[randint(0,3)])


#pedra papel tesoura
@bot.command(pass_context=True)
async def rps(ctx, player):
    if(player == 'rock' or player == 'paper' or player == 'scissors'  or player == 'r' or player == 'p' or player == 's'):
        cpu = getRPS()
        player = simpRPS(player)
        result = "**JBB won!**" #assume que o JBB ganha
        if (player == cpu):
            result = "**It´s a tie!**"
        if (player == "rock" and cpu == "scissors"):
            result = "**You won!**"
        if (player == "paper" and cpu == "rock"):
            result = "**You won!**"
        if (player == "scissors" and cpu == "paper"):
            result = "**You won!**"
        await bot.say('You played ' + player + '\nJBB played ' + cpu + '\n' + result)
    else:
        await bot.say('*Invalid*')


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
