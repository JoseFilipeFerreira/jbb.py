import discord
import asyncio
import json
from discord.ext import commands
from random import randint

bot = commands.Bot(command_prefix = '*')

bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(a:int, b:int):
    await bot.say(a + b)

########################################################

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

########################################################

@bot.command(pass_context=True)
async def roll(ctx):
    await bot.say('You rolled a ' + str(randint(1,20)))

@bot.command(pass_context=True)
async def flip(ctx):
    n = randint(0,10000)
    line = 'WTF the coin landed upright!'
    if(n<5000): line = 'You got tails'
    elif(n<10000): line = 'You got heads'

    await bot.say(line)

@bot.command(pass_context=True)
async def pick(ctx):
    simbolo = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei']
    naipe = ['paus', 'ouros', 'copas', 'espadas']
    await bot.say(simbolo[randint(0,12)] + ' de ' + naipe[randint(0,3)])


#@bot.command(pass_context=True)
#async def helpPlay(ctx):
#    with open('./modules/menus.json') as menusFile:
#        menus = json.load(menusFile)
#        await bot.say(menus['helpPlay'] + musicFiles.join('\n'))      

bot.run(open('auth').readline().rstrip())