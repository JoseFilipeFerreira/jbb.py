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

cogs_blacklist = []

def main():
    #adding to bot object directories
    bot.IMAGES_PATH = './Media/Images/'
    bot.GIFS_PATH = './Media/Gif/'
    bot.MUSIC_PATH = './Media/Music/'
    bot.TMP_PATH = './Media/Tmp/'
    bot.BATTLEROYALE_PATH = './modules/battleroyale.json'
    bot.BATTLEROYALEWINS_PATH = './modules/battleroyalewins.json'
    bot.BATTLEROYALEKDR_PATH = './modules/battleroyalekdr.json'
    bot.EXTENSIONS_PATH ='Extensions'
    
    #default color for embeds (yellow)
    bot.embed_color = 0xffff00

    #adding to bot object available media
    bot.imagesMap = {}
    bot.gifsMap = {}
    bot.musicMap = {}

    #load media
    for f in os.listdir(bot.IMAGES_PATH):
        if path.isfile(path.join(bot.IMAGES_PATH, f)):
            filename, _ = path.splitext(f)
            bot.imagesMap[filename.lower()] = f

    for f in os.listdir(bot.GIFS_PATH):
        if path.isfile(path.join(bot.GIFS_PATH, f)):
            filename, _ = path.splitext(f)
            bot.gifsMap[filename.lower()] = f

    for f in os.listdir(bot.MUSIC_PATH):
        if path.isfile(path.join(bot.MUSIC_PATH, f)):
            filename, _ = path.splitext(f)
            bot.musicMap[filename.lower()] = f

    #load extensions
    extensions_loader(create_list_extensions())

    bot.voice_client = None
    bot.player_client = None
    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='*help'))

    embed = discord.Embed(
        title="Starting up",
        description="bot started at " + str(datetime.now()),
        color=bot.embed_color)

    embed.add_field(
        name="Extensions loaded",
        value=bot.extensions_list_loaded,
        inline=True)
    
    embed.add_field(
        name="Extensions failed",
        value=bot.extensions_list_failed,
        inline=True)
    
    blacklist = "No Cogs in Blaklist"
    if len(cogs_blacklist) > 0:
        blacklist = '\n'.join(cogs_blacklist)

    embed.add_field(
        name="Blacklist",
        value=blacklist,
        inline=False)

    appInfo = await bot.application_info()

    await bot.send_message(appInfo.owner, embed=embed)

    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------------------------')
    print('Servers:')
    for server in bot.servers:
        print(server.name)
    print('-----------------------------')
    print(bot.command_prefix)

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



def create_list_extensions():
#create a list with possible extensions
    extensions_list = os.listdir(bot.EXTENSIONS_PATH + '/')
    
    def extension_splitter(x):
        extension, _ = path.splitext(x)
        return extension
    
    extensions_list = list(
        map(
            lambda x : extension_splitter(x),
            extensions_list
        ))
    
    extensions_list = list(
        filter(
            lambda x: "__" not in x and x not in cogs_blacklist,
            extensions_list
        ))
    
    return(extensions_list)

def extensions_loader(extensions):
#try to load extensions
    loaded = ""
    failed = ""
    for extension in extensions:
        try:
            bot.load_extension(bot.EXTENSIONS_PATH + '.' + extension)
            loaded = loaded + "\n" + extension
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension: {}\n{}'.format(extension, exc))
            failed = failed + "\n" + ('**{}**:{}'.format(extension, exc))
    
    bot.extensions_list_loaded = loaded
    bot.extensions_list_failed = "No cogs failed to load"
    if not failed == "": bot.extensions_list_failed = failed

def checkArray(tester, s):
    result = False
    for test in tester:
        result = result or test in s
    return result

main()
