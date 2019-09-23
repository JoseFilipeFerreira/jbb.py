import discord
import json
import subprocess
from random import randint
from discord.ext import commands

class Interact(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='hug',
                      description="hug somenone you love",
                      brief="hug somenone you love")
    async def hug(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("You have to tell me who to hug!")
        elif size > 1:
            await ctx.send("Calm down! Hug one at a time!")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("You can't fake human interaction like that!")
        else:
            await ctx.send("c⌒っ╹v╹ )っ {0}  received a hug from {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='slap',
                      description="slap somenone you hate",
                      brief="slap somenone you hate")
    async def slap(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("You have to tell me who to slap!")
        elif size > 1:
            await ctx.send("Calm down! You have two hands but can only slap one at a time!")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("You can't slap yourself! Well... You shouldn't.")
        else:
            await ctx.send("( ‘д‘ ⊂ 彡☆))Д´) {0} received a slap from {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='punch',
                      description="punch someone you hate",
                      brief="punch someone you hate")
    async def punch(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("You have to tell me who to punch!")
        elif size > 1:
            await ctx.send("Calm down! I advise you to first punch the worst one!")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("You can punch yourself! But first you should get some help.")
        else:
            await ctx.send("(*＇Д＇)ﾉｼ)ﾟﾛﾟ ) {0} was punched by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))
    
    @commands.command(name='whip',
                      description="whip the sinner",
                      brief="whip the sinner")
    async def whip(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("You have to tell me who to whip!")
        elif size > 1:
            await ctx.send("I know you are kinky, but please whip one at a time!")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("Perhaps you sould ask someone to do that for you.")
        else:
            await ctx.send("(˵ ͡~ ͜ʖ ͡°˵)ﾉ⌒{0} was whipped by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='table',
                      description="show the world you are flipping a table",
                      brief="flip a table")
    async def table(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("Tell me who made you flip tables!")
        elif size > 1:
            await ctx.send("It is not healthy to flip more than one table at once.")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("You shouldn't make yourself flip tables.")
        else:
            await ctx.send("(╯°□°）╯︵ ┻━┻ {0} just made {1} flip.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='snipe',
                      description="shoot that guy down",
                      brief="snipe someone")
    async def snipe(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("Tell me who to snipe!")
        elif size > 1:
            await ctx.send("You are using a sniper. Not a minigun.")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("you could just do a flip.")
        elif randint(0,9) == 0:
            await ctx.send("Oh no! You failed the shot, like everything you do in your life.")
        else:
            await ctx.send("︻デ═一 {0} was sniped by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='giveup',
                      description="give up on humanity",
                      brief="give up on humanity")
    async def giveup(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("Tell me who made you lose fate in humanity!")
        elif size > 1:
            await ctx.send("You should lose hope in one person at a time.")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("You matter, unless you multiply yourself by ligthspeed then you energy.")
        else:
            await ctx.send("¯\\_( ツ )_/¯ {0} just made {1} lose hope in humanity.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='tbag',
                      description="tbag that noob",
                      brief="tbag that noob")
    async def tbag(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("Tell me who to humiliate!")
        elif size > 1:
            await ctx.send("You only have one bag to tbag.")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("I can't picture a pose in wich this is possible.")
        else:
            await ctx.send("( ﾟДﾟ)┌┛Σ( ﾟ∀ﾟ)･∵ {0}, the last thing you see before you die  is {1} tbag.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='angry',
                      description="show the world that someone made you angry",
                      brief="show you are angry")
    async def angry(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("Tell me who pissed you off!")
        elif size > 1:
            await ctx.send("It is better to direct anger at only one person at a time.")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("Keep it to yourself then.")
        else:
            await ctx.send("( ╬ Ò ‸ Ó) {0} just made {1} angry.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='touch',
                      description="touch that special someone",
                      brief="touch that special someone")
    async def touch(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("Tell me who to touch!")
        elif size > 1:
            await ctx.send("Direct your love to one person at a time.")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("Touch yourself in private!")
        else:
            await ctx.send("( ͡° ͜ʖ ͡°) {0} was gently touched by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    @commands.command(name='lick',
                      description="lick like an icecream",
                      brief="lick like an icecream")
    async def lick(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("Tell me who to lick!")
        elif size > 1:
            await ctx.send("You only have one tongue.")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("Stop licking yourself! It is unsanitary")
        else:
            await ctx.send("(っˆڡˆς){0} was licked by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))

    commands.command(name='duel',
                      description="duel that guy, but remenber, you migth lose",
                      brief="duel someone")
    async def duel(self, ctx):
        size = len(ctx.message.mentions)
        if size == 0:
            await ctx.send("Tell me who is your opponent!")
        elif size > 1:
            await ctx.send("You can only do 1v1.")
        elif ctx.message.author in ctx.message.mentions:
            await ctx.send("Stop trying to fight your inner demons")
        else:
            if randint(0,99) > 49: await ctx.send("(ᗒᗣᗕ)՞o==|::::::::::::> {0} was wrecked by {1}.".format(ctx.message.mentions[0].mention, ctx.message.author.mention))
            else: await ctx.send("(ᗒᗣᗕ)՞o==|::::::::::::> {0} was wrecked by {1}.".format(ctx.message.author.mention, ctx.message.mentions[0].mention))

def setup(bot):
    bot.add_cog(Interact(bot))
