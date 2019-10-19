import discord
from discord.ext import commands
import asyncio
import datetime
import json
from random import choice
from aux.misc import round_down
from aux.stats import Stats

class BattleRoyale(commands.Cog):
    """BattleRoyale in the server"""
    def __init__(self, bot):
        self.bot = bot
        self.listAction = ["kill", "die", "event", "meet"]
        self.listReactions = json.load(open(bot.BATTLEROYALE_PATH, 'r'))
        
    @commands.command(name='battleroyaleFull',
                      description="create server wide battle royale [ADMIN ONLY]\n\nWinner gets 100 coins.",
                      brief="server wide battle royale",
                      aliases=['brF'])
    @commands.has_permissions(administrator=True)
    async def battleroyaleFull(self, ctx):
        await ctx.message.delete()
        await sendChallenge(self, ctx)
        users = correctListUsers(ctx, ctx.message.guild.members)
        await sendAllDailyReports(self, ctx, users)

        embed = victoryEmbed(self, users["alive"][0])
        await ctx.send(embed=embed)

        self.bot.stats.give_cash(users["alive"][0]["id"], 100)
        
        updateStats(self, users)
    
    @commands.command(name='battleroyale',
                      description="create server battle royale",
                      brief="server battle royale",
                      aliases=['br'])
    @commands.is_nsfw()
    async def battleroyale(self, ctx):
        await ctx.message.delete()
        msg = await sendChallenge(self, ctx)
        async with ctx.message.channel.typing():
            await asyncio.sleep(20)

        msg = await msg.channel.fetch_message(msg.id)

        members = []
        for reaction in msg.reactions:
            members += await reaction.users().flatten()

        users = correctListUsers(ctx, members)
        
        if len(users["alive"]) < 2:
            await ctx.send("Not enough players for a Battle Royale")
            return

        await sendAllDailyReports(self, ctx, users)

        embed = victoryEmbed(self, users["alive"][0])
        await ctx.send(embed=embed)

        updateStats(self, users)
    
    @commands.command(name='battleroyaleKDR',
                      description="battleroyale Kill/Death Ratio",
                      brief="battleroyale Kill/Death Ratio",
                      aliases=['brKDR', 'KDR'])
    async def battleroyaleKDR(self, ctx, member : discord.Member = None):
        if member:
            win = get_stat(self.bot, member.id)
            embed = discord.Embed(
                title = 'Battleroyale no DI',
                description="KDR Leaderboard",
                color=self.bot.embed_color)

            embed.add_field(
                name=member.display_name,
                value="KDR: {0}/{1}".format(win["kills"], win["death"]),
            inline=False)
            await ctx.send(embed=embed)
            return

        arrayKDR = []
        for id in self.bot.stats.get_all_users():
            k, d = self.bot.get_kdr(id)
            kdr = {
                "id": id,
                "kills": k,
                "death": d}
            arrayKDR.append(kdr)
        
        def compare(kdr):
            if kdr["death"] == 0:
                return 0
            return kdr["kills"] / kdr["death"]

        arrayKDR.sort(key=compare, reverse=True)

        embed = discord.Embed(
            title = 'Battleroyale no DI',
            description="KDR Leaderboard",
            color=self.bot.embed_color)

        for i in range(3):
            win = arrayKDR[i]
            member = ctx.message.guild.get_member(win["id"])
            embed.add_field(
                name=f"{i+1}. {member.display_name}",
                value=f"KDR: {win['kills']}/{win['death']}",
                inline=False)
            
        embed.set_thumbnail(
            url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png")

        await ctx.send(embed=embed)

    @commands.command(name='addBattleroyale',
                      brief="add a Battleroyale event",
                      aliases=['addBr'])
    @commands.is_owner()
    async def addBattleroyale(self, ctx, action, time : float,*, description = None):
        """add a Battleroyale event to the json [OWNER ONLY]
        __**action**__:
        * **kill** A was killed by B
        * **die** A died
        * **event** something happened to A
        * **meet"** A met B
        __**time**__:
        * t <= 12"""
        action = action.lower()
        time = round(time, 1)
        time = round_down(time * 10, 5)
        time = time /10
        if not description:
            await ctx.send('Invalid description')
            return
        
        if action not in self.listAction:
            await ctx.send('Invalid action')
            return

        if time <= 0 or time > 12:
            await ctx.send('Invalid time')
            return

        event = {
            "action":self.listAction.index(action),
            "time":time,
            "description":description}
        self.listReactions.append(event)
        updateListActions(self)
        await ctx.send("**action:**`{0}`\n**time:**`{1}`h\n**description:**`{2}`".format(action, time, description))  

    @commands.command(name='deleteBattleroyale',
                      description="delete the last Battleroyale event on the json [OWNER ONLY]",
                      brief="remove last Battleroyale event",
                      aliases=['removeBattleroyale', 'removeBr', 'deleteBr'])
    @commands.is_owner()
    async def deleteBattleroyale(self, ctx):
        deleted = self.listReactions.pop()
        updateListActions(self)
        await ctx.send(
            "__**DELETED**__\n**action:**`{0}`\n**time:**`{1}`h\n**description:**`{2}`"
                .format(
                    deleted["action"],
                    deleted["time"],
                    deleted["description"]))  

async def sendChallenge(self, ctx):
    embed = discord.Embed(
        title = 'Battle Royale no DI',
        description='{} started a battle royale'.format(ctx.message.author.mention),
        color=self.bot.embed_color)

    embed.set_thumbnail(
        url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png")

    embed.add_field(
        name='Pick your weapon below if you wish to participate',
        value='(you have approximately 30 seconds)')

    msg = await ctx.send(embed=embed)
    await msg.add_reaction('🔫')

    return await ctx.fetch_message(msg.id)

async def sendAllDailyReports(self, ctx, users):
#gets a list of all users and sends all days
    #check if enough users
    await sendInitialReport(self, ctx)
    day = 1
    time = getCurrentHour()
    while(len(users["alive"]) > 1):
        figthTrailer, users = generateDailyReport(self, ctx, users, time)
        await sendDaylyReport(self, ctx, day, figthTrailer)
        time = 24
        day += 1

def generateDailyReport(self, ctx, users, time):
#generates a string with a daily report and returns a list containing survivors
    figthTrailer = []
    while(len(users["alive"]) > 1 and time > 0):
        match = choice(self.listReactions)
        if time - match["time"] <= 0:
            break
        elif match["action"] == 0: #kill
            p1 = choice(users["alive"])
            users["alive"].remove(p1)
            users["dead"].append(p1)

            p2 = choice(users["alive"])
            p2["kills"] += 1

            figthResult = match["description"].format(p1["name"], p2["name"])

        elif match["action"] == 1: #die
            p1 = choice(users["alive"])
            users["alive"].remove(p1)
            users["dead"].append(p1)

            figthResult = match["description"].format(p1["name"])
        elif match["action"] == 2: #event
            p1 = choice(users["alive"])

            figthResult = match["description"].format(p1["name"])

        elif match["action"] == 3: #meet
            p1 = choice(users["alive"])
            p2 = choice(users["alive"])

            figthResult = match["description"].format(p1["name"], p2["name"])
        
        time = time - match["time"]
        figthTrailer.append("**" + convertHour(time) + "** " + figthResult)

    return "\n".join(figthTrailer), users

async def sendDaylyReport(self, ctx, day, result):
#send a embed with the daily report
    if result == "": result = "Today nothing happened"
    embed = discord.Embed(
        title = 'DAY {}'.format(day),
        description=result,
        color=self.bot.embed_color)

    await ctx.send(embed=embed)

async def sendInitialReport(self,ctx):
#send first embed of report
    embed = discord.Embed(
        title = 'Battle Royale no DI',
        description='Result of the battle',
        color=self.bot.embed_color)

    embed.set_thumbnail(
        url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png")

    await ctx.send(embed=embed)

def correctListUsers(ctx, users):
#takes a list of users and gives a list of user name/nick an id
    users = list(filter(lambda x: not x.bot, users))

    def changeNick(user):
        member = ctx.message.guild.get_member(user.id)
        return {
            "name": member.display_name,
            "id": user.id,
            "kills": 0}

    users = list(map(changeNick , users))
    users = [i for n, i in enumerate(users) if i not in users[n+1:]]
    return {"alive": users, "dead": []}

def victoryEmbed(self, user):
#create final embed
    embed = discord.Embed(
        title = 'Winner',
        description=user["name"],
        color=self.bot.embed_color)

    embed.set_footer(text = "Kills: {}".format(user["kills"]))
    return embed

def getCurrentHour():
#gets current hour irl
    now = datetime.datetime.now()
    time = 24 - now.hour
    if now.minute > 30:
        time = time - 1
    elif now.minute > 0:
        time = time - 0.5
    return time

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

def updateListActions(self):
#update a JSON file
    with open(self.bot.BATTLEROYALE_PATH, 'w') as file:
        json.dump(self.listReactions, file, indent=4)

def updateStats(self, users):
#update Stats JSON file
    for user in users["dead"]:
        self.bot.stats.update_kills(user["id"], 1, user["kills"], 0)
    for user in users["alive"]:
        self.bot.stats.update_kills(user["id"], 0, user["kills"], 1)

    self.bot.stats.save_stats()

def setup(bot):
    bot.add_cog(BattleRoyale(bot))
