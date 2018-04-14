import discord
import asyncio
import json
from discord.ext import commands
from random import randint
from datetime import datetime

bot = commands.Bot(command_prefix = '*')

bot.remove_command('help')

#log variabels
registo = '**Log pedidos JBB:**'
nregisto = 0

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(a:int, b:int):
    await bot.say(a + b)


######################################################## HELP


@bot.command(pass_context=True)
async def info(ctx):
    with open('./package.json') as infoFile:
        info = json.load(menusFile)
        await bot.say('**' + info['description'] + '**\n\nCreated by: *' + info['author'] + '*\nVersion: *' + info['version'] + '*\n\n`*help` for commands')


@bot.command(pass_context=True)
async def help(ctx):
    with open('./modules/menus.json') as menusFile:
        menus = json.load(menusFile)
        await bot.say(menus['help'])


@bot.command(pass_context=True)
async def helpP(ctx):
    with open('./modules/menus.json') as menusFile:
        menus = json.load(menusFile)
        await bot.say(menus['helpP'])


@bot.command(pass_context=True)
async def helpG(ctx):
    with open('./modules/menus.json') as menusFile:
        menus = json.load(menusFile)
        await bot.say(menus['helpG'])


@bot.command(pass_context=True)
async def helpquote(ctx):
    with open('./modules/menus.json') as menusFile:
        menus = json.load(menusFile)
        await bot.say(menus['helpquote'])


#@bot.command(pass_context=True)
#async def helpPlay(ctx):
#    with open('./modules/menus.json') as menusFile:
#        menus = json.load(menusFile)
#        await bot.say(menus['helpPlay'] + musicFiles.join('\n')) 

######################################################## GAMES

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


#Macro to update the log
#def loggergenerator(userName, identifier):
#    nspaces = 40 - userName.length - identifier.length
#    currentdate = datetime.now()
#    var datetime = currentdate.date()   + "/"
#                 + currentdate.month()  + "/" 
#                 + currentdate.year()   + " @ "  
#                 + currentdate.hour()   + ":"  
#                 + currentdate.minute() + ":" 
#                 + currentdate.second()
#    
#    registo = registo + '\n*' + userName + identifier + '*' + '\n' + datetime
#    print(userName + identifier + ' '.repeat(nspaces) + datetime)
#    logwriter.write('\n' + userName + identifier + ' '.repeat(nspaces) + datetime)
#    nregisto++
#    prevDate = currentdate   
    


bot.run(open('auth').readline().rstrip())