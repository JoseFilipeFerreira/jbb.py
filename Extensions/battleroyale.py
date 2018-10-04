import discord
from discord.ext import commands
import random
from random import randint
from random import choice
import asyncio
import json


class BattleRoyale():
    
    def __init__(self, bot):
        self.bot = bot
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

        figthTrailer = ""
        while(len(users) > 1):
            #choose the one that is killed and the one who kills
            p1 = choice(users)
            users.remove(p1)
            p2 = choice(users)


            figthResult = choice(self.listReactions)["description"].format(p1, p2)
            figthTrailer = figthTrailer + figthResult + "\n"
        #create final embed
        embed = discord.Embed(
            title = 'Battle Royale no DI',
            description='Result of the battle',
            color=self.bot.embed_color
        )
        embed.set_thumbnail(
        url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png"
        )
        embed.add_field(
            name = 'Fights',
            value=figthTrailer,
            inline=False
        )
        embed.add_field(
            name='Winner',
            value=users[0],
            inline=False
        )
        await self.bot.say(embed=embed)   

async def sendDaylyReport(self, ctx, day, result):
    embed = discord.Embed(
        title = 'DAY {}'.format(day),
        description=result,
        color=self.bot.embed_color
    )
    await self .bot.send_message(ctx.message.channel, embed=embed)

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
        name='Pick your weapon bellow if you wish to participate',
        value='(you have approximately 30 seconds)'
    )
    msg = await self.bot.send_message(ctx.message.channel,embed=embed)
    await self.bot.add_reaction(msg, '\U0001F52B')
    #update sent embed so it contains the reaction
    return await self.bot.get_message(msg.channel, msg.id)


def setup(bot):
    bot.add_cog(BattleRoyale(bot))