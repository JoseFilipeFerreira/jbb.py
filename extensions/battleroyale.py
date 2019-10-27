import discord
from discord.ext import commands
import asyncio
import json
from datetime import datetime
from random import choice
from aux.misc import round_down
from aux.stats import Stats

class InvalidNumberPlayers(Exception):
    pass

class Warrior():
    def __init__(self, member):
        self.member = member
        self.kills = 0

    def add_Kill(self):
        self.kills += 1

    def get_name(self):
        return self.member.display_name

    def get_id(self):
        return self.member.id

    def get_kills(self):
        return self.kills

class Battle():
    def __init__(self, listReactions, embed_color, members):
        self.listReactions = listReactions
        self.embed_color = embed_color
        self.alive = set()
        self.dead = set()
        for member in members:
            if not member.bot:
                self.alive.add(Warrior(member))
        if len(self.alive) < 2:
            raise InvalidNumberPlayers()

        self.day = 1

        now = datetime.now()
        self.time = 24 - now.hour
        if now.minute > 30:
            self.time -= 1
        elif now.minute > 0:
            self.time -= 0.5
    
    def initialReport(self):
        embed = discord.Embed(
            title = 'Battle Royale no DI',
            description=f'Result of the battle\nParticipants: {len(self.alive)}',
            color=self.embed_color)
        embed.set_thumbnail(
            url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png")
        return embed

    def get_winner(self):
        winner = self.alive.pop()
        self.alive.add(winner)
        return winner

    def victoryEmbed(self):
        winner = self.get_winner()
        embed = discord.Embed(
            title = 'Winner',
            description=winner.get_name(),
            color=self.embed_color)
        embed.set_footer(text = f"Kills: {winner.get_kills()}")
        return embed

    def allReports(self):
        yield self.initialReport()
        while(len(self.alive) > 1):
            yield self.dailyReportEmbed()
            self.time = 24
            self.day += 1
        yield self.victoryEmbed()

    def dailyReportEmbed(self):
        result = self.dailyReport()
        if not result:
            result = "Today nothing happened"
        embed = discord.Embed(
            title = f'DAY {self.day}',
            description='\n'.join(result),
            color=self.embed_color)
        return embed

    def dailyReport(self):
        figthTrailer = []
        while(len(self.alive) > 1 and self.time > 0):
            match = choice(self.listReactions)

            if self.time - match["time"] <= 0:
                break
            elif match["action"] == 0: #kill
                p1 = choice(tuple(self.alive))
                self.alive.remove(p1)
                self.dead.add(p1)
    
                p2 = choice(tuple(self.alive))
                p2.add_Kill()
    
                figthResult = match["description"].format(p1.get_name(), p2.get_name())
    
            elif match["action"] == 1: #die
                p1 = choice(tuple(self.alive))
                self.alive.remove(p1)
                self.dead.add(p1)
    
                figthResult = match["description"].format(p1.get_name())

            elif match["action"] == 2: #event
                p1 = choice(tuple(self.alive))
                figthResult = match["description"].format(p1.get_name())
    
            elif match["action"] == 3: #meet
                p1 = choice(tuple(self.alive))
                p2 = choice(tuple(self.alive))
    
                figthResult = match["description"].format(p1.get_name(), p2.get_name())
            self.time -= match["time"]
            figthTrailer.append("**" + self.displayTime() + "** " + figthResult)
    
        return figthTrailer

    def displayTime(self):
    #convert time in hours to midnigth to hour of day
        time = 24 - self.time
        minutes = time * 60
        hours, minutes = divmod(minutes, 60)
        hours = int(hours)
        minutes = int(minutes)
        if hours < 10:
            hours = "0{}".format(hours)
        if minutes < 10:
            minutes = "0{}".format(minutes)
        return "{0}:{1}h".format(hours, minutes)

    def updateStats(self, stats):
        for warrior in self.dead:
            stats.update_kills(warrior.get_id(), 1, warrior.get_kills(), 0)
        for warrior in self.alive:
            stats.update_kills(warrior.get_id(), 0, warrior.get_kills(), 1)
        stats.save_stats()


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

        br = Battle(self.listReactions, self.bot.embed_color, ctx.message.guild.members)
        for embed in br.allReports():
            await ctx.send(embed=embed)

        self.bot.stats.give_cash(br.get_winner().get_id(), 100)
        br.updateStats(self.bot.stats)
    
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

        members = set()
        for reaction in msg.reactions:
            members.update(await reaction.users().flatten())

        try:
            br = Battle(self.listReactions, self.bot.embed_color, members)
        except InvalidNumberPlayers:
            await ctx.send("Not enough players for a Battle Royale")
            return

        for embed in br.allReports():
            await ctx.send(embed=embed)

        br.updateStats(self.bot.stats)
    
    @commands.command(name='battleroyaleKDR',
                      description="battleroyale Kill/Death Ratio",
                      brief="battleroyale Kill/Death Ratio",
                      aliases=['brKDR', 'KDR'])
    async def battleroyaleKDR(self, ctx, member : discord.Member = None):
        if member:
            k, d = self.bot.stats.get_kdr(member.id)
            embed = discord.Embed(
                title = 'Battleroyale no DI',
                description="KDR Leaderboard",
                color=self.bot.embed_color)

            embed.add_field(
                name=member.display_name,
                value="KDR: {0}/{1}".format(k, d),
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


def updateListActions(self):
#update a JSON file
    with open(self.bot.BATTLEROYALE_PATH, 'w') as file:
        json.dump(self.listReactions, file, indent=4)

def setup(bot):
    bot.add_cog(BattleRoyale(bot))
