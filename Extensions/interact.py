import discord
import json
import subprocess
from random import randint
from discord.ext import commands

class Interact(commands.Cog):
    """Interact with other users while pinging them"""    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='hug',
                      description="hug somenone you love",
                      brief="hug somenone you love")
    async def hug(self, ctx):
        await send_msg(
            ctx,
            "You have to tell me who to hug!",
            "Calm down! Hug one at a time!",
            "You can't fake human interaction like that!",
            "c⌒っ╹v╹ )っ {0}  received a hug from {1}.")


    @commands.command(name='slap',
                      description="slap somenone you hate",
                      brief="slap somenone you hate")
    async def slap(self, ctx):
        await send_msg(
            ctx,
            "You have to tell me who to slap!",
            "Calm down! You have two hands but can only slap one at a time!",
            "You can't slap yourself! Well... You shouldn't.",
            "( ‘д‘ ⊂ 彡☆))Д´) {0} received a slap from {1}.")

    @commands.command(name='punch',
                      description="punch someone you hate",
                      brief="punch someone you hate")
    async def punch(self, ctx):
        await send_msg(
            ctx,
            "You have to tell me who to punch!",
            "Calm down! I advise you to first punch the worst one!",
            "You can punch yourself! But first you should get some help.",
            "(*＇Д＇)ﾉｼ)ﾟﾛﾟ ) {0} was punched by {1}.")
    
    @commands.command(name='whip',
                      description="whip the sinner",
                      brief="whip the sinner")
    async def whip(self, ctx):
        await send_msg(
            ctx,
            "You have to tell me who to whip!",
            "I know you are kinky, but please whip one at a time!",
            "Perhaps you sould ask someone to do that for you.",
            "(˵ ͡~ ͜ʖ ͡°˵)ﾉ⌒{0} was whipped by {1}.")

    @commands.command(name='table',
                      description="show the world you are flipping a table",
                      brief="flip a table")
    async def table(self, ctx):
        await send_msg(
            ctx,
            "Tell me who made you flip tables!",
            "It is not healthy to flip more than one table at once.",
            "You shouldn't make yourself flip tables.",
            "(╯°□°）╯︵ ┻━┻ {0} just made {1} flip.")

    @commands.command(name='giveup',
                      description="give up on humanity",
                      brief="give up on humanity")
    async def giveup(self, ctx):
        await send_msg(
            ctx,
            "Tell me who made you lose fate in humanity!",
            "You should lose hope in one person at a time.",
            "You matter, unless you multiply yourself by ligthspeed then you energy.",
            "¯\\_( ツ )_/¯ {0} just made {1} lose hope in humanity.")

    @commands.command(name='tbag',
                      description="tbag that noob",
                      brief="tbag that noob")
    async def tbag(self, ctx):
        await send_msg(
            ctx,
            "Tell me who to humiliate!",
            "You only have one bag to tbag.",
            "I can't picture a pose in wich this is possible.",
            "( ﾟДﾟ)┌┛Σ( ﾟ∀ﾟ)･∵ {0}, the last thing you see before you die  is {1} tbag.")

    @commands.command(name='angry',
                      description="show the world that someone made you angry",
                      brief="show you are angry")
    async def angry(self, ctx):
        await send_msg(
            ctx,
            "Tell me who pissed you off!",
            "It is better to direct anger at only one person at a time.",
            "Keep it to yourself then.",
            "( ╬ Ò ‸ Ó) {0} just made {1} angry.")

    @commands.command(name='touch',
                      description="touch that special someone",
                      brief="touch that special someone")
    async def touch(self, ctx):
        await send_msg(
            ctx,
            "Tell me who to touch!",
            "Direct your love to one person at a time.",
            "Touch yourself in private!",
            "( ͡° ͜ʖ ͡°) {0} was gently touched by {1}.")

    @commands.command(name='lick',
                      description="lick like an icecream",
                      brief="lick like an icecream")
    async def lick(self, ctx):
        await send_msg(
            ctx,
            "Tell me who to lick!",
            "You only have one tongue.",
            "Stop licking yourself! It is unsanitary",
            "(っˆڡˆς){0} was licked by {1}.")

    @commands.command(name='snipe',
                      description="shoot that guy down",
                      brief="snipe someone")
    async def snipe(self, ctx):
        await send_msg(
            ctx,
            "Tell me who to snipe!",
            "You are using a sniper. Not a minigun.",
            "you could just do a flip.",
            "Oh no! You failed the shot, like everything you do in your life." if randint(0,9) == 0 else "︻デ═一 {0} was sniped by {1}.")

    @commands.command(name='duel',
                      description="duel that guy, but remenber, you migth lose",
                      brief="duel someone")
    async def duel(self, ctx):
        await send_msg(
            ctx,
            "Tell me who is your opponent!",
            "You can only do 1v1.",
            "Stop trying to fight your inner demons",
            "(ᗒᗣᗕ)՞o==|::::::::::::> {0} was wrecked by {1}." if randint(0,99) > 49 else "(ᗒᗣᗕ)՞o==|::::::::::::> {0} was wrecked by {1}.")

def setup(bot):
    bot.add_cog(Interact(bot))

async def send_msg(ctx, no_user, several_user, self_user, correct_message):
    size = len(ctx.message.mentions)
    if size == 0:
        await ctx.send(no_user)
    elif size > 1:
        await ctx.send(several_user)
    elif ctx.message.author in ctx.message.mentions:
        await ctx.send(self_user)
    else:
        await ctx.send(correct_message.format(
            ctx.message.mentions[0].mention,
            ctx.message.author.mention))

