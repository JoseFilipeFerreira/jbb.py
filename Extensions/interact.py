import discord
import json
import subprocess
from random import randint
from discord.ext import commands
from random import randint

class Interact():
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='hug',
                      description="hug somenone you love",
                      brief="hug somenone you love",
                      pass_context=True)
    async def hug(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("You have to tell me who to hug!")
        elif size > 1:
            await self.bot.say("Calm down! Hug one at a time!")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("You can't fake human interaction like that!")
        else:
            await self.bot.say("c⌒っ╹v╹ )っ {0}  received a hug from {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='slap',
                      description="slap somenone you hate",
                      brief="slap somenone you hate",
                      pass_context=True)
    async def slap(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("You have to tell me who to slap!")
        elif size > 1:
            await self.bot.say("Calm down! You have two hands but can only slap one at a time!")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("You can't slap yourself! Well... You shouldn't.")
        else:
            await self.bot.say("( ‘д‘ ⊂ 彡☆))Д´) {0} received a slap from {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='punch',
                      description="punch someone you hate",
                      brief="punch someone you hate",
                      pass_context=True)
    async def punch(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("You have to tell me who to punch!")
        elif size > 1:
            await self.bot.say("Calm down! I advise you to first punch the worst one!")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("You can punch yourself! But first you should get some help.")
        else:
            await self.bot.say("(*＇Д＇)ﾉｼ)ﾟﾛﾟ ) {0} was punched by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))
    
    @commands.command(name='whip',
                      description="whip the sinner",
                      brief="whip the sinner",
                      pass_context=True)
    async def whip(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("You have to tell me who to whip!")
        elif size > 1:
            await self.bot.say("I know you are kinky, but please whip one at a time!")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("Perhaps you sould ask someone to do that for you.")
        else:
            await self.bot.say("(˵ ͡~ ͜ʖ ͡°˵)ﾉ⌒{0} was whipped by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='table',
                      description="show the world you are flipping a table",
                      brief="flip a table",
                      pass_context=True)
    async def table(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("Tell me who made you flip tables!")
        elif size > 1:
            await self.bot.say("It is not healthy to flip more than one table at once.")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("You shouldn't make yourself flip tables.")
        else:
            await self.bot.say("(╯°□°）╯︵ ┻━┻ {0} just made {1} flip.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='snipe',
                      description="shoot that guy down",
                      brief="snipe someone",
                      pass_context=True)
    async def snipe(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("Tell me who to snipe!")
        elif size > 1:
            await self.bot.say("You are using a sniper. Not a minigun.")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("you could just do a flip.")
        elif randint(0,9) == 0:
            await self.bot.say("Oh no! You failed the shot, like everything you do in your life.")
        else:
            await self.bot.say("︻デ═一 {0} was sniped by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='giveup',
                      description="give up on humanity",
                      brief="give up on humanity",
                      pass_context=True)
    async def giveup(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("Tell me who made you lose fate in humanity!")
        elif size > 1:
            await self.bot.say("You should lose hope in one person at a time.")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("You matter, unless you multiply yourself by ligthspeed then you energy.")
        else:
            await self.bot.say("¯\\_( ツ )_/¯ {0} just made {1} lose hope in humanity.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='tbag',
                      description="tbag that noob",
                      brief="tbag that noob",
                      pass_context=True)
    async def tbag(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("Tell me who to humiliate!")
        elif size > 1:
            await self.bot.say("You only have one bag to tbag.")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("I can't picture a pose in wich this is possible.")
        else:
            await self.bot.say("( ﾟДﾟ)┌┛Σ( ﾟ∀ﾟ)･∵ {0}, the last thing you see before you die  is {1} tbag.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='angry',
                      description="show the world that someone made you angry",
                      brief="show you are angry",
                      pass_context=True)
    async def angry(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("Tell me who pissed you off!")
        elif size > 1:
            await self.bot.say("It is better to direct anger at only one person at a time.")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("Keep it to yourself then.")
        else:
            await self.bot.say("( ╬ Ò ‸ Ó) {0} just made {1} angry.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='touch',
                      description="touch that special someone",
                      brief="touch that special someone",
                      pass_context=True)
    async def touch(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("Tell me who to touch!")
        elif size > 1:
            await self.bot.say("Direct your love to one person at a time.")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("Touch yourself in private!")
        else:
            await self.bot.say("( ͡° ͜ʖ ͡°) {0} was gently touched by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='lick',
                      description="lick like an icecream",
                      brief="lick like an icecream",
                      pass_context=True)
    async def lick(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("Tell me who to lick!")
        elif size > 1:
            await self.bot.say("You only have one tongue.")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("Stop licking yourself! It is unsanitary")
        else:
            await self.bot.say("(っˆڡˆς){0} was licked by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    commands.command(name='duel',
                      description="duel that guy, but remenber, you migth lose",
                      brief="duel someone",
                      pass_context=True) 
    async def duel(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await self.bot.say("Tell me who is your opponent!")
        elif size > 1:
            await self.bot.say("You can only do 1v1.")
        elif ctx.message.author in ctx.message.mentions:
            await self.bot.say("Stop trying to fight your inner demons")
        else:
            if randint(0,99) > 49: await self.bot.say("(ᗒᗣᗕ)՞o==|::::::::::::> {0} was wrecked by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))
            else: await self.bot.say("(ᗒᗣᗕ)՞o==|::::::::::::> {0} was wrecked by {1}.".format(ctx.message.author.mention, ctx.message.mentions[0].mention))

def setup(bot):
    bot.add_cog(Interact(bot))
