import discord
from discord.ext import commands
import asyncio 
import json
import traceback
from datetime import datetime
from os import path, listdir
from aux.stats import Stats

bot = commands.Bot(
    command_prefix = '>',
    case_insensitive=True)

bot.remove_command('help')

cogs_blacklist = []

def main():
    #adding to bot object directories
    bot.IMAGES_PATH = './Media/Images/'
    bot.GIFS_PATH = './Media/Gif/'
    bot.MUSIC_PATH = './Media/Music/'
    bot.TMP_PATH = './Media/Tmp/'
    bot.QUOTES_PATH = './db/quotes.json'
    bot.GAMES_PATH ='./Media/Games/'
    bot.BATTLEROYALE_PATH = './db/battleroyale.json'
    bot.STATS_PATH = './db/stats.json'
    bot.BIOGRAPHY_PATH = './db/biography.json'
    bot.EXTENSIONS_PATH ='extensions'
    bot.MARKET_PATH='./db/market.json'
    bot.IMPACT_PATH='.db/impact.ttf'
    bot.REPLIES_PATH='./db/replies.json'
   
    #load media
    bot.imagesMap = {}
    for f in listdir(bot.IMAGES_PATH):
        if path.isfile(path.join(bot.IMAGES_PATH, f)):
            filename, _ = path.splitext(f)
            bot.imagesMap[filename.lower()] = f

    bot.gifsMap = {}
    for f in listdir(bot.GIFS_PATH):
        if path.isfile(path.join(bot.GIFS_PATH, f)):
            filename, _ = path.splitext(f)
            bot.gifsMap[filename.lower()] = f

    bot.musicMap = {}
    for f in listdir(bot.MUSIC_PATH):
        if path.isfile(path.join(bot.MUSIC_PATH, f)):
            filename, _ = path.splitext(f)
            bot.musicMap[filename.lower()] = f
    
    #load stats
    bot.stats = Stats(bot.STATS_PATH)

    #load market
    bot.replies       = json.load(open(bot.REPLIES_PATH, 'r'))

    #load extensions
    extensions_loader(create_list_extensions())
    
    #voice
    bot.voice_client = None
    bot.player_client = None

    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='*help'))

    #default color for embeds
    bot.embed_color = get_bot_color(bot)

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

    await appInfo.owner.send(embed=embed)

    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------------------------')
    print('Servers:')
    for guild in bot.guilds:
        print(guild.name)
    print('-----------------------------')
    print(bot.embed_color)
    print(bot.command_prefix)


@bot.event
async def on_message(message):
	await reactMessage(message)

@bot.event
async def on_message_edit(before, after):
	await reactMessage(after)

async def reactMessage(message):
    if message.content.lower() in bot.replies:
        await message.channel.send(
            bot.replies[message.content.lower()])

    #send media
    if message.content.startswith(bot.command_prefix):
        content = message.content.lower()[1:]
        if content in bot.imagesMap:
            await message.channel.send(
                file = discord.File(
                    bot.IMAGES_PATH+bot.imagesMap[content]))
            return
        elif content in bot.gifsMap:
            await message.channel.send_file(
                file = discord.File(
                    bot.GIFS_PATH+bot.gifsMap[content]))
            return

    #exit voice channel
    if bot.player_client != None and bot.player_client.is_playing() == False:
        await bot.voice_client.disconnect()
        bot.voice_client = None
        bot.player_client = None
    
    #coin giveaway
    given = bot.stats.daily_giveaway(10)
    if given:
        appInfo = await bot.application_info()
        await appInfo.owner.send("Giveaway: {}".format(given))

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    bot.stats.add_user(member.id)
    bot.stats.save_stats()

@bot.event
async def on_member_remove(member):
    bot.stats.remove_user(member.id)
    bot.stats.save_stats(bot)

def get_bot_color(bot):
    bGuild, color = 0, 0xffff00
    for guild in bot.guilds:
        if len(guild.members) > bGuild:
            bGuild, color = len(guild.members), guild.me.color
    return color

def create_list_extensions():
#create a list with possible extensions
    extensions_list = listdir(bot.EXTENSIONS_PATH + '/')
    
    def extension_splitter(x):
        extension, _ = path.splitext(x)
        return extension
    
    extensions_list = list(map(extension_splitter, extensions_list))
    
    extensions_list = list(filter(
            lambda x: "__" not in x and x not in cogs_blacklist,
            extensions_list))
    
    return sorted(extensions_list)

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
            print(f'Failed to load extension: {extension}\n{exc}')
            failed = failed + "\n" + ('**{}**:{}'.format(extension, exc))
            print(traceback.format_exc())
    
    bot.extensions_list_loaded = loaded
    bot.extensions_list_failed = "No cogs failed to load"
    if failed != "": bot.extensions_list_failed = failed

main()
