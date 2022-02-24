import discord
import time
from discord.ext import commands
import asyncio
import json
import traceback
from datetime import datetime
from os import path, listdir
from aux.stats import Stats
from aux.misc import minutes_passed
import yaml

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix = '*',
    case_insensitive=True,
    intents=intents)

bot.remove_command('help')

cogs_blacklist = []

def main():
    #adding to bot object directories
    bot.MEDIA_PATH = './media/'
    bot.TMP_PATH = '/tmp/'
    bot.GAMES_PATH ='./assets/'
    bot.QUOTES_PATH = './db/quotes.json'
    bot.BATTLEROYALE_PATH = './db/battleroyale.json'
    bot.STATS_PATH = './db/stats.json'
    bot.BIOGRAPHY_PATH = './db/biography.json'
    bot.EXTENSIONS_PATH ='extensions'
    bot.MARKET_PATH='./db/market.json'
    bot.IMPACT_PATH='./db/impact.ttf'
    bot.REPLIES_PATH='./db/replies.json'
    bot.SLOWMODE_PATH='./db/slow.json'
    bot.IP_PATH='./ip.txt'
    bot.DOTFILES_PATH='./db/dotfiles.json'

    with open("config.yaml", "r") as f:
        bot.config = yaml.safe_load(f)

    #load media
    bot.mediaMap = {}
    for f in listdir(bot.MEDIA_PATH):
        if path.isfile(path.join(bot.MEDIA_PATH, f)):
            filename, _ = path.splitext(f)
            bot.mediaMap[filename.lower()] = f

    #load stats
    bot.stats = Stats(bot.STATS_PATH)

    bot.replies = json.load(open(bot.REPLIES_PATH, 'r'))

    #load slowmode
    bot.slow_users = json.load(open(bot.SLOWMODE_PATH, 'r'))

    #load extensions
    extensions_loader(create_list_extensions())

    bot.run(bot.config['credentials']['discord'])

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
    if message.content.lower() in bot.replies:
        await message.channel.send(
            bot.replies[message.content.lower()])

    #send media
    if message.content.startswith(bot.command_prefix):
        slowed_user = bot.slow_users['users'].get(str(message.author.id), None)
        if slowed_user is not None:
            bot.slow_users['users'][str(message.author.id)] = time.time()
            with open(bot.SLOWMODE_PATH, 'w', encoding='utf8') as file:
                json.dump(bot.slow_users, file, indent=4)
            if minutes_passed(slowed_user, time.time()) <= bot.slow_users['time']:
                await message.author.send("You are in the JBB naughty list, this meaning that you can only call a command one every {} minutes. Be carefull, every time you try to call a command before the cooldown ends, it will start again".format(bot.slow_users['time']))
                return
        content = message.content.lower()[1:]
        if content in bot.mediaMap:
            await message.channel.send(
                file = discord.File(
                    bot.MEDIA_PATH+bot.mediaMap[content]))
            return

    #coin giveaway
    bot.stats.daily_giveaway(10)

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    bot.stats.add_user(member.id)
    nUser = len(list(filter(lambda x: not x.bot , member.guild.members)))
    if nUser % 100 == 0:
        await member.guild.system_channel.send(f"🎉 **CONGRATULATIONS** 🎉\nYou are the user number {nUser}\nClick here to redeem your prize -> <https://bit.ly/MIEIreward>")
    bot.stats.save_stats()

@bot.event
async def on_member_remove(member):
    bot.stats.remove_user(member.id)
    bot.stats.save_stats()

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
