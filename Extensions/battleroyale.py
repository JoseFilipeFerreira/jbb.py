import discord
from discord.ext import commands
import random
import datetime
from random import randint
from random import choice
import asyncio
import json


class BattleRoyale():
    
    def __init__(self, bot):
        self.bot = bot
        self.listAction = ["kill", "die", "event"]
        self.listReactions=[]
        with open(bot.BATTLEROYALE_PATH, 'r') as file:
            self.listReactions = json.load(file)
    
    @commands.command(pass_context=True)
    async def battleroyale(self, ctx):
    #TODO: make it so that people don't cry by seeing this piece of code
    #create battle royale
        if ctx.message.channel.name not in ['nsfw', 'bot-commands']:
            await self.bot.say(
                "This command must be done in #nsfw or #bot-commands"
            )
            return
        await self.bot.delete_message(ctx.message)
        msg = await sendChallenge(self, ctx)
        await thirtysecondtyping(self, ctx)
        users = await getListUsers(self, ctx, msg.reactions[0])

        #check if enough users
        if len(users) < 2:
            await self.bot.say("Not enough players for a Battle Royale")
            return
        
        await sendInitialReport(self, ctx)

        day = 1
        time = getCurrentHour()
        while(len(users) > 1):
            figthTrailer, users = generateDailyReport(self, ctx, users, time)
            await sendDaylyReport(self, ctx, day, figthTrailer)
            time = 24
            day = day + 1

        #create final embed
        embed = discord.Embed(
            title = 'Winner',
            description=users[0],
            color=self.bot.embed_color
        )
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def addBattleroyale(self, ctx, action, time,*, description):
    #add a Battleroyale description
        appInfo = await self.bot.application_info()
        owner = appInfo.owner
        action = action.lower()
        time = round(float(time), 1)
        time = round_down(time * 10, 5)
        time = time /10
        #TODO optimize one day
        if ctx.message.author != owner:
            await self.bot.say('Invalid user')

        elif len(description) < 1:
            await self.bot.say('Invalid description')
        
        elif action not in self.listAction:
            await self.bot.say('Invalid action')

        elif time <= 0 or time > 12:
            await self.bot.say('Invalid time')

        else:
            event = {
                "action":self.listAction.index(action),
                "time":time,
                "description":description
            }
            print(event)
            self.listReactions.append(event)
            updateListReactions(self)
            await self.bot.say("**action:**`{0}`\n**time:**`{1}`h\n**description:**`{2}`".format(action, time, description))  

    @commands.command(pass_context=True)
    async def deleteBattleroyale(self, ctx):
    #add a Battleroyale description
        appInfo = await self.bot.application_info()
        owner = appInfo.owner
        #TODO optimize one day
        if ctx.message.author != owner:
            await self.bot.say('Invalid user')
        else:
            deleted = self.listReactions.pop()
            updateListReactions(self)
            await self.bot.say(
                "__**DELETED**__\n**action:**`{0}`\n**time:**`{1}`h\n**description:**`{2}`"
                    .format(
                        deleted["action"],
                        deleted["time"],
                        deleted["description"]
                    )
            )  

def getCurrentHour():
#gets current hour irl
    now = datetime.datetime.now()
    time = 24 - now.hour
    if now.minute > 30:
        time = time - 1
    elif now.minute > 0:
        time = time - 0.5
    return time

def generateDailyReport(self, ctx, users, time):
#generates a string with a daily report and returns a list containing survivors
    figthTrailer = ""
    while(len(users) > 1 and time > 0):
        match = choice(self.listReactions)
        if time - match["time"] < 0:
            break
        elif match["action"] == 0:
            p1 = choice(users)
            users.remove(p1)
            p2 = choice(users)

            figthResult = match["description"].format(p1, p2)
        elif match["action"] == 1:
            p1 = choice(users)
            users.remove(p1)

            figthResult = match["description"].format(p1)
        else: #action default
            p1 = choice(users)

            figthResult = match["description"].format(p1)
        
        time = time - match["time"]
        figthTrailer = figthTrailer + "**" + convertHour(time) + "** " + figthResult + "\n"

    return figthTrailer, users

async def sendDaylyReport(self, ctx, day, result):
#send a embed with the daily report
    if result == "": result = "Today nothing happened"
    embed = discord.Embed(
        title = 'DAY {}'.format(day),
        description=result,
        color=self.bot.embed_color
    )
    await self .bot.send_message(ctx.message.channel, embed=embed)

async def sendInitialReport(self,ctx):
#send first embed of report
    embed = discord.Embed(
        title = 'Battle Royale no DI',
        description='Result of the battle',
        color=self.bot.embed_color
    )
    embed.set_thumbnail(
    url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png"
    )
    await self.bot.say(embed=embed)

async def thirtysecondtyping(self, ctx):
#wait 30 seconds for people to join while typing
    await self.bot.send_typing(ctx.message.channel)
    await asyncio.sleep(9)
    await self.bot.send_typing(ctx.message.channel)
    await asyncio.sleep(9)
    await self.bot.send_typing(ctx.message.channel)
    await asyncio.sleep(9)

async def getListUsers(self, ctx, reaction):
#create a list with the users that reacted
    users = await self.bot.get_reaction_users(reaction)
    users = list(filter(lambda x: not x.bot, users))

    def changeNick(user):
        member = ctx.message.server.get_member(user.id)
        if member.nick != None:
            return member.nick
        else:
            return member.name

    users = list(map(changeNick , users))

    return list(set(users))

async def sendChallenge(self, ctx):
#generate embed
    embed = discord.Embed(
        title = 'Battle Royale no DI',
        description='{} started a battle royale'.format(ctx.message.author.mention),
        color=self.bot.embed_color
    )
    embed.set_thumbnail(
        url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png"
    )
    embed.add_field(
        name='Pick your weapon below if you wish to participate',
        value='(you have approximately 30 seconds)'
    )
    msg = await self.bot.send_message(ctx.message.channel,embed=embed)
    await self.bot.add_reaction(msg, '\U0001F52B')
    #update sent embed so it contains the reaction
    return await self.bot.get_message(msg.channel, msg.id)

def round_down(num, divisor):
#round down a num to the nearest multiple of a divisor
    return num - (num%divisor)

def convertHour(time):
#convert time in hours to midnigth to hour of day
    time = 24 - time
    minutes = time * 60
    hours, minutes = divmod(minutes, 60)
    hours = int(hours)
    minutes = int(minutes)
    if hours < 10:
        hours = "0{}".format(hours)
    if minutes < 10:
        minutes = "0{}".format(minutes)
    return "{0}:{1}h".format(hours, minutes)

def updateListReactions(self):
#update a JSON file
    with open(self.bot.BATTLEROYALE_PATH, 'w') as file:
        json.dump(self.listReactions, file, indent=4)

def setup(bot):
    bot.add_cog(BattleRoyale(bot))
