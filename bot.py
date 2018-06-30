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

#log variabels
registo = '**Log pedidos JBB:**'
nregisto = 0

extensions = ['games','quotes', 'programming','api', 'pokemon', 'ascii', 'youtube', 'menu', 'manage', 'memegenerator']

imagesMap = {}
gifsMap = {}
musicMap = {}

voice_client = None
player_client = None

IMAGES_PATH = './Images/'
GIFS_PATH = './Gif/'
MUSIC_PATH = './Music/'

def main():
    for f in os.listdir(IMAGES_PATH):
        if path.isfile(path.join(IMAGES_PATH, f)):
            filename, file_ext = path.splitext(f)
            imagesMap[filename.lower()] = f

    for f in os.listdir(GIFS_PATH):
        if path.isfile(path.join(GIFS_PATH, f)):
            filename, file_ext = path.splitext(f)
            gifsMap[filename.lower()] = f

    for f in os.listdir(MUSIC_PATH):
        if path.isfile(path.join(MUSIC_PATH, f)):
            filename, file_ext = path.splitext(f)
            musicMap[filename.lower()] = f

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='*help'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
	await reactMessage(message)

@bot.event
async def on_message_edit(before, after):
	await reactMessage(after)


async def reactMessage(message):
    if (message.content.lower() == 'push %ebp'):
        await bot.send_message(message.channel, 'pop %recurso')
    if message.content.startswith('*'):
        content = message.content.lower()[1:]
        if content in imagesMap:
            await bot.send_file(
                message.channel, IMAGES_PATH+imagesMap[content])
            return
        elif content in gifsMap:
            await bot.send_file(
                message.channel, GIFS_PATH+gifsMap[content])
            return
    await bot.process_commands(message)

    global player_client
    global voice_client
    if player_client != None and player_client.is_playing() == False:
        await voice_client.disconnect()
        voice_client = None
        player_client = None

@bot.event
async def on_member_join(member):
    server = member.server
    await bot.send_message(server.get_channel('418433020719136770'), 'Welcome to Selva MIEI! {0}'.format(member.mention))

######################################################## MÚSICA
@bot.command(pass_context=True)
async def play(ctx, music):
    if ctx.message.author.voice_channel:
        if music in musicMap:
            global voice_client
            global player_client
            if voice_client == None:
               voice = await bot.join_voice_channel(ctx.message.author.voice_channel)
               voice_client = voice
            if player_client != None and player_client.is_playing():
                await bot.say("Already Playing")
            else:
                player = voice_client.create_ffmpeg_player(MUSIC_PATH + music + ".mp3")
                player_client = player
                player.start()
        else:
        	await bot.say("Invalid Music")
    else:
    	await bot.say("You're not in a voice channel")

@bot.command(pass_context=True)
async def stop(ctx):
    if ctx.message.author.voice_channel:
        global voice_client
        global player_client
        if voice_client:
            await voice_client.disconnect()
            voice_client = None
            player_client = None
        else:
        	await bot.say("JBB not in a voice channel")
    else:
    	await bot.say("You're not in a voice channel")

main()
