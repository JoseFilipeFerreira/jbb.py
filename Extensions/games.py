import discord
from discord.ext import commands
import random
from random import randint
from random import choice
import asyncio


class Games():
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def roll(self, ctx, nfaces=20):
    #atirar um dado com 20 faces
        await self.bot.say('You rolled a ' + str(randint(1,nfaces)))
    

    @commands.command(pass_context=True)
    async def flip(self, ctx):
    #atirar moeda ao ar (com easteregg)
        n = randint(0,10000)
        line = 'WTF the coin landed upright!'
        if(n<5000): line = 'You got tails'
        elif(n<10000): line = 'You got heads'
    
        await self.bot.say(line)
    
    
    @commands.command(pass_context=True)
    async def pick(self, ctx):
    #escolher uma carta
        simbolo = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei']
        naipe = ['paus', 'ouros', 'copas', 'espadas']
        await self.bot.say(choice(simbolo) + ' de ' + choice(naipe))
    
    
    @commands.command(pass_context=True)
    async def rps(self, ctx, player):
    #pedra papel tesoura
        if(player in ['rock','paper','scissors','r','p','s']):
            cpu = choice(['rock','paper','scissors'])
            player = simpRPS(player)
            result = "**JBB won!**" #assume que o JBB ganha top kek
            if (player == cpu):
                result = "**It´s a tie!**"
            if (player == "rock" and cpu == "scissors"):
                result = "**You won!**"
            if (player == "paper" and cpu == "rock"):
                result = "**You won!**"
            if (player == "scissors" and cpu == "paper"):
                result = "**You won!**"
            await self.bot.say('You played ' + player + '\nJBB played ' + cpu + '\n' + result)
        else:
            await self.bot.say('*Invalid*')
    
    
    @commands.command(pass_context=True)
    async def choose(self, ctx, *choices : str):
    #escolhe entre vários argumentos passados
        """Chooses between multiple choices."""
        if all(('@' not in choice) for choice in choices):
            await self.bot.say(choice(choices))

    
    @commands.command()
    async def magicball(self):
    #dá resposta positiva ou negativa
        a = ['Most likely', 'Very doubtful', 'Ask again', 'As I see it, yes', 'My sources say no', 'Cannot perdict now', 'Yes', 'Dont count on it', 'Without a doubt', 'Better not tell you']
        await self.bot.say(choice(a))

    
    @commands.command(pass_context=True)
    async def guess(self, ctx):
    #guess coin
        await self.bot.say("Guess how the coin landed (head/tail)")
        
        def guess_check(m):
            return m.content.lower() == 'tail' or m.content.lower() == 'head'
        
        await self.bot.send_typing(ctx.message.channel)
        guess = await self.bot.wait_for_message(
            timeout=10.0,
            author=ctx.message.author,
            check=guess_check)

        n = randint(0,1)
        answer  = 'tail'
        if(n==1): answer = 'head'

        if guess is None:
            await self.bot.say('You took too long. I got {}'.format(answer))
        elif guess.content == answer:
            await self.bot.say('You guessed it!')
        else:
            await self.bot.say("You're wrong. I got {}".format(answer))

    
    @commands.command(pass_context=True)
    async def vote(self, ctx, *quote):
    #create poll
        if not quote:
           quote = 'Vote here'
        else:
           quote = ' '.join(word for word in quote)
        await self.bot.delete_message(ctx.message)
        vote = await self.bot.say('**{0}** (poll by {1})'.format(quote, ctx.message.author.mention))
        await self.bot.add_reaction(vote, '\U0000274C')
        await self.bot.add_reaction(vote, '\U00002705')

    @commands.command(pass_context=True)
    async def battleroyale(self, ctx):
    #create battle royale
        if ctx.message.channel.name not in ['nsfw', 'bot-commands']:
            await self.bot.say("This command must be done in #nsfw or #bot-commands")
            return
        await self.bot.delete_message(ctx.message)
        #generate embed
        embed = discord.Embed(
            title = 'Battle Royale no DI',
            description='{} started a battle royale'.format(ctx.message.author.mention),
            color=0xffff00
        )
        embed.set_thumbnail(url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png")
        embed.add_field(name='Pick your weapon bellow if you wish to participate', value='(you have approximately 10 seconds)')
        msg = await self.bot.say(embed=embed)
        await self.bot.add_reaction(msg, '\U0001F52B')
        #update sent embed so it contains the reaction
        msg = await self.bot.get_message(msg.channel, msg.id)
        await self.bot.send_typing(ctx.message.channel)
        #wait 10 seconds for people to join
        await asyncio.sleep(10)
        #create a list with the users that reacted
        users = await self.bot.get_reaction_users(msg.reactions[0])
        users = list(set(users[:-1]))

        listReactions=[
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
            "This masrks the last time {0} saw {1}. {1} is a dick.",
            "One for the money, two for show, {0} is dead, {1} made him blow.",
            "Much like my ex {0} got fucked by {1}.",
            "Are you Microft {0}? Because {1} mada an Apple out of you."
        ]
        figthTrailer = ""
        while(len(users) > 1):
            #choose the one that is killed and the one who kills
            p1 = randint(0, len(users)-1)
            p2 = randint(0, len(users)-1)
            if p1 == p2:
                if p2 == (len(users) - 1): p2 = p2 - 1
                else: p2 = p2 + 1

            killed = users[p1]
            killer = users[p2]
            users.pop(p1)

            figthResult = choice(listReactions).format(killed.name, killer.name)
            figthTrailer = figthTrailer + figthResult + "\n"
        #create final embed
        embed = discord.Embed(
            title = 'Battle Royale no DI',
            description='Result of the battle',
            color=0xffff00
        )
        embed.set_thumbnail(url="https://mbtskoudsalg.com/images/pubg-lvl-3-helmet-png-7.png")
        embed.add_field(
            name='Fights',
            value=figthTrailer
        )
        embed.add_field(
            name='Winner',
            value=users[0].name
        )
        await self.bot.say(embed=embed)

def getRPS():
    n = randint(0,2)
    if(n == 0):
        return "rock"
    if(n == 1):
        return "paper"
    return "scissors"


def simpRPS(hand):
    if (hand == "r"):
        hand = "rock"
    if (hand == "p"):
        hand = "paper"
    if (hand == "s"):
        hand = "scissors"
    return hand
    

def setup(bot):
    bot.add_cog(Games(bot))
