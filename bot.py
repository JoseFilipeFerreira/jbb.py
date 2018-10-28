import discord
import asyncio
import json
from discord.ext import commands
from datetime import datetime
import os
from os import path
import subprocess

bot = commands.Bot(command_prefix = '*')

bot.remove_command('help')

extensions = [
    'games',
    'quotes',
    'programming',
    'api',
    'pokemon',
    'ascii',
    'youtube',
    'menu',
    'manage',
    'memegenerator',
    'interact',
    'music',
    'battleroyale'
]


def main():
    #adding to bot object directories
    bot.IMAGES_PATH = './Media/Images/'
    bot.GIFS_PATH = './Media/Gif/'
    bot.MUSIC_PATH = './Media/Music/'
    bot.TMP_PATH = './Media/Tmp/'
    bot.BATTLEROYALE_PATH = './modules/battleroyale.json'
    bot.BATTLEROYALEWINS_PATH = './modules/battleroyalewins.json'
    bot.EXTENSIONS_PATH ='Extensions.'
    
    #default color for embeds (yellow)
    bot.embed_color = 0xffff00

    #adding to bot object available media
    bot.imagesMap = {}
    bot.gifsMap = {}
    bot.musicMap = {}

    #load media
    for f in os.listdir(bot.IMAGES_PATH):
        if path.isfile(path.join(bot.IMAGES_PATH, f)):
            filename, file_ext = path.splitext(f)
            bot.imagesMap[filename.lower()] = f

    for f in os.listdir(bot.GIFS_PATH):
        if path.isfile(path.join(bot.GIFS_PATH, f)):
            filename, file_ext = path.splitext(f)
            bot.gifsMap[filename.lower()] = f

    for f in os.listdir(bot.MUSIC_PATH):
        if path.isfile(path.join(bot.MUSIC_PATH, f)):
            filename, file_ext = path.splitext(f)
            bot.musicMap[filename.lower()] = f

    #load extensions
    for extension in extensions:
        try:
            bot.load_extension(bot.EXTENSIONS_PATH + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.voice_client = None
    bot.player_client = None
    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='*help'))

    print('Logged in as:')
    print('> ' +bot.user.name)
    print('> ' +bot.user.id)
    print('-----------------------------')
    print('Servers:')
    for server in bot.servers:
        print('> ' + server.name)

@bot.event
async def on_message(message):
	await reactMessage(message)

@bot.event
async def on_message_edit(before, after):
	await reactMessage(after)

async def reactMessage(message):
    if (message.content.lower() == 'push %ebp'):
        await bot.send_message(message.channel, 'pop %recurso')

    if message.content.startswith(bot.command_prefix):
        content = message.content.lower()[1:]
        if content in bot.imagesMap:
            await bot.send_file(
                message.channel, bot.IMAGES_PATH+bot.imagesMap[content])
            return
        elif content in bot.gifsMap:
            await bot.send_file(
                message.channel, bot.GIFS_PATH+bot.gifsMap[content])
            return

    if bot.player_client != None and bot.player_client.is_playing() == False:
        await bot.voice_client.disconnect()
        bot.voice_client = None
        bot.player_client = None

    await bot.process_commands(message)




def checkArray(tester, s):
    result = False
    for test in tester:
        result = result or test in s
    return result

main()
