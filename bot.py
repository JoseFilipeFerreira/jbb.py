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
    with open('./package.json') as menusFile:
        info = json.load(menusFile)
        await bot.say('**' + info['description'] + '**\n\nCreated by: *' + info['author'] + '*\nVersion: *' + info['version'] + '*\n\n`*help` for commands')


@bot.command(pass_context=True)
async def help(ctx):
    with open('./modules/menus.json') as menusFile:
        menus = json.load(menusFile)
        await bot.send_message(ctx.message.author, menus['help'])
        await bot.delete_message(ctx.message)


@bot.command(pass_context=True)
async def helpP(ctx):
    with open('./modules/menus.json') as menusFile:
        menus = json.load(menusFile)
        await bot.send_message(ctx.message.author, menus['helpP'])
        await bot.delete_message(ctx.message)


@bot.command(pass_context=True)
async def helpG(ctx):
    with open('./modules/menus.json') as menusFile:
        menus = json.load(menusFile)
        await bot.send_message(ctx.message.author, menus['helpG'])
        await bot.delete_message(ctx.message)


@bot.command(pass_context=True)
async def helpquote(ctx):
    with open('./modules/menus.json') as menusFile:
        menus = json.load(menusFile)
        await bot.send_message(ctx.message.author, menus['helpquote'])
        await bot.delete_message(ctx.message)


#@bot.command(pass_context=True)
#async def helpPlay(ctx):
#    with open('./modules/menus.json') as menusFile:
#        menus = json.load(menusFile)
#        await bot.say(menus['helpPlay'] + musicFiles.join('\n')) 


######################################################## QUOTES
@bot.command(pass_context=True)
async def quote(ctx):
    await bot.say(getRLine('quote'))


@bot.command(pass_context=True)
async def quoteA(ctx):
    await bot.say(getRLine('quoteA'))


@bot.command(pass_context=True)
async def fact(ctx):
    await bot.say(getRLine('fact'))


@bot.command(pass_context=True)
async def nquoteA(ctx):
    await bot.say('Existem ' + getNLine('quoteA') + ' quotes de alunos')


@bot.command(pass_context=True)
async def nquote(ctx):
    await bot.say('Existem ' + getNLine('quote') + ' quotes do JBB')


@bot.command(pass_context=True)
async def nfact(ctx):
    await bot.say('Existem '+ getNLine('fact') + ' factos sobre o JBB')


@bot.command(pass_context=True)
async def ntotal(ctx):
    n = str(int(getNLine('quote')) + int(getNLine('quoteA')) + int(getNLine('fact')))
    await bot.say('Existem '+ n + ' frases')


def getRLine(filename):
    file = open("./modules/quotes/" + filename + ".txt")
    quotes_array = file.read().split('\n-\n')
    return quotes_array[randint(0, len(quotes_array) -1 )]

def getNLine(filename):
    file = open("./modules/quotes/" + filename + ".txt")
    quotes_array = file.read().split('\n-\n')
    return str(len(quotes_array))


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

######################################################## MÚSICA
@bot.command(pass_context=True)
async def play(ctx, music):
    voice_channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(voice_channel)
    voice_channel.play(discord.FFmpegPCMAudio('./Music' + music +'.mp3'))


######################################################## PIADAS

####################################PNG
@bot.command(pass_context=True)
async def oracle(ctx):
    await bot.say(':bat:')


@bot.command(pass_context=True)
async def sapos1(ctx):
    await bot.say(':frog:')


@bot.command(pass_context=True)
async def hitler(ctx):
    await bot.say('<:burger_hitler:418524889624870912>')


@bot.command(pass_context=True)
async def herulume(ctx):
    await bot.say('top kek')

                
@bot.command(pass_context=True)
async def denied(ctx):
    await bot.send_file(ctx.message.channel,'Images/denied.png')


@bot.command(pass_context=True)
async def survival(ctx):
    await bot.send_file(ctx.message.channel,'Images/survival.png')


@bot.command(pass_context=True)
async def sugoi(ctx):
    await bot.send_file(ctx.message.channel,'Images/sugoi.png')


@bot.command(pass_context=True)
async def rude(ctx):
    await bot.send_file(ctx.message.channel,'Images/rude.png')


@bot.command(pass_context=True)
async def dont(ctx):
    await bot.send_file(ctx.message.channel,'Images/dont.png')


@bot.command(pass_context=True)
async def milady(ctx):
    await bot.send_file(ctx.message.channel,'Images/milady.png')


@bot.command(pass_context=True)
async def manilator(ctx):
    await bot.send_file(ctx.message.channel,'Images/manilator.png')


@bot.command(pass_context=True)
async def mac(ctx):
    await bot.send_file(ctx.message.channel,'Images/mac.png')  


@bot.command(pass_context=True)
async def nani(ctx):
    await bot.send_file(ctx.message.channel,'Images/nani.png')


@bot.command(pass_context=True)
async def arroz(ctx):
    await bot.send_file(ctx.message.channel,'Images/arroz.png') 


@bot.command(pass_context=True)
async def deusvult(ctx):
    await bot.send_file(ctx.message.channel,'Images/deusvult.png')


@bot.command(pass_context=True)
async def coffee(ctx):
    await bot.send_file(ctx.message.channel,'Images/coffee.png')


@bot.command(pass_context=True)
async def morning(ctx):
    await bot.send_file(ctx.message.channel,'Images/morning.png')


@bot.command(pass_context=True)
async def confused(ctx):
    await bot.send_file(ctx.message.channel,'Images/confused.png')


@bot.command(pass_context=True)
async def notateacher(ctx):
    await bot.send_file(ctx.message.channel,'Images/notateacher.png')


@bot.command(pass_context=True)
async def question(ctx):
    await bot.send_file(ctx.message.channel,'Images/question.png')


@bot.command(pass_context=True)
async def wtf(ctx):
    await bot.send_file(ctx.message.channel,'Images/wtf.png')


@bot.command(pass_context=True)
async def fly(ctx):
    await bot.send_file(ctx.message.channel,'Images/fly.png')


@bot.command(pass_context=True)
async def cena(ctx):
    await bot.send_file(ctx.message.channel,'Images/cena.png')


@bot.command(pass_context=True)
async def doubt(ctx):
    await bot.send_file(ctx.message.channel,'Images/doubt.png')


@bot.command(pass_context=True)
async def anime(ctx):
    await bot.send_file(ctx.message.channel,'Images/anime.png')


@bot.command(pass_context=True)
async def mendess(ctx):
    await bot.send_file(ctx.message.channel,'Images/mendess.png')


####################################GIF


@bot.command(pass_context=True)
async def perfection(ctx):
    await bot.send_file(ctx.message.channel,'Images/perfection.gif')


@bot.command(pass_context=True)
async def dodge(ctx):
    await bot.send_file(ctx.message.channel,'Images/dodge.gif')


####################################SOUND PNG


@bot.command(pass_context=True)
async def dorifto(ctx):
    await bot.send_file(ctx.message.channel,'Images/dorifto.png')


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