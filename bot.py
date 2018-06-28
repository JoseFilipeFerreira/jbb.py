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

@bot.event
async def on_member_join(member):
    server = member.server
    await bot.send_message(server.get_channel('418433020719136770'), 'Welcome to Selva MIEI! {0}'.format(member.mention))

######################################################## MÚSICA
#@bot.command(pass_context=True)
#async def play(ctx, music):
#    voice_channel = ctx.message.author.voice.voice_channel
#    await bot.join_voice_channel(voice_channel)
#    voice_channel.play(discord.FFmpegPCMAudio('./Music' + music +'.mp3'))


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
