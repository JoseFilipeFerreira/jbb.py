import discord
import asyncio
import json
from discord.ext import commands
from datetime import datetime
import os
from os import path

bot = commands.Bot(command_prefix = '*')

bot.remove_command('help')

#log variabels
registo = '**Log pedidos JBB:**'
nregisto = 0

extensions = ['games','quotes']
imagesMap = {}
gifsMap = {}

IMAGES_PATH = './Images/'
GIFS_PATH = './Gif/'

def main():
    for f in os.listdir(IMAGES_PATH):
        if path.isfile(path.join(IMAGES_PATH, f)):
            filename, file_ext = path.splitext(f)
            imagesMap[filename.lower()] = f

    for f in os.listdir(GIFS_PATH):
        if path.isfile(path.join(GIFS_PATH, f)):
            filename, file_ext = path.splitext(f)
            gifsMap[filename.lower()] = f

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    bot.run(open('auth').readline().rstrip())


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    if message.content.startswith('*'):
        content = message.content.lower()[1:]
        if content in imagesMap:
            await bot.send_file(
                message.channel, IMAGES_PATH+imagesMap[content])
        elif content in gifsMap:
            await bot.send_file(
                message.channel, GIFS_PATH+gifsMap[content])

    await bot.process_commands(message)


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


######################################################## MÚSICA
@bot.command(pass_context=True)
async def play(ctx, music):
    voice_channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(voice_channel)
    voice_channel.play(discord.FFmpegPCMAudio('./Music' + music +'.mp3'))

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
    


main()