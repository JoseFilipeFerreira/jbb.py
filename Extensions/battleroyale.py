import discord
from discord.ext import commands
import random
from random import randint
from random import choice
import asyncio


class BattleRoyale():
    
    def __init__(self, bot):
        self.bot = bot
        self.listReactions=[
            "{0}'s cold body was tbaged by {1}.",
            "{0} was sniped by {1}.",
            "{0} had an heart attack from {1}'s face.",
            "{0} was 360 noscoped by {1}.",
            "{0}'s head will make a nice addition to {1}'s collection.",
            "{0}'s meat was a little too bland for {1}'s taste.",
            "{0}'s scared dead face made {1}'s day.",
            "{0}'s blood will make a delicious drink for {1}.",
            "{0}'s anus was wrecked by {1}.",
            "{0}'s body, much like Java, was killed by {1}",
            "This marks the last time {0} saw {1}. {1} is a dick.",
            "One for the money, two for show, {0} is dead, {1} made him blow.",
            "Much like my ex {0} got fucked by {1}.",
            "Are you Microsoft {0}? Because {1} mada an Apple out of you."
        ]

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
        msg = await self.bot.say(embed=embed)
        await self.bot.add_reaction(msg, '\U0001F52B')
        #update sent embed so it contains the reaction
        msg = await self.bot.get_message(msg.channel, msg.id)
        
        #wait 30 seconds for people to join while typing
        await self.bot.send_typing(ctx.message.channel)
        await asyncio.sleep(9)
        await self.bot.send_typing(ctx.message.channel)
        await asyncio.sleep(9)
        await self.bot.send_typing(ctx.message.channel)
        await asyncio.sleep(9)

        #create a list with the users that reacted
        users = await self.bot.get_reaction_users(msg.reactions[0])
        users = list(filter(lambda x: not x.bot, users))
        users = list(set(users))

        def changeNick(user):
            member = ctx.message.server.get_member(user.id)
            if member.nick != None:
                return member.nick
            else:
                return member.name

        users = list(map(changeNick , users))

        
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


            figthResult = choice(self.listReactions).format(p1, p2)
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
            name='Fights',
            value=figthTrailer,
            inline=False
        )
        embed.add_field(
            name='Winner',
            value=users[0],
            inline=False
        )
        await self.bot.say(embed=embed)   

def setup(bot):
    bot.add_cog(BattleRoyale(bot))