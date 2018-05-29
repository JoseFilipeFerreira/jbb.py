import discord
from discord.ext import commands
import random
from random import randint
from random import choice


class Games():
    
    def __init__(self, bot):
        self.bot = bot


    #atirar um dado com 20 faces
    @commands.command(pass_context=True)
    async def roll(self, ctx, nfaces=20):
        await self.bot.say('You rolled a ' + str(randint(1,nfaces)))
    
    
    #atirar moeda ao ar (com easteregg)
    @commands.command(pass_context=True)
    async def flip(self, ctx):
        n = randint(0,10000)
        line = 'WTF the coin landed upright!'
        if(n<5000): line = 'You got tails'
        elif(n<10000): line = 'You got heads'
    
        await self.bot.say(line)
    
    
    #escolher uma carta
    @commands.command(pass_context=True)
    async def pick(self, ctx):
        simbolo = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei']
        naipe = ['paus', 'ouros', 'copas', 'espadas']
        await self.bot.say(choice(simbolo) + ' de ' + choice(naipe))
    
    
    #pedra papel tesoura
    @commands.command(pass_context=True)
    async def rps(self, ctx, player):
        if(player in ['rock','paper','scissors','r','p','s']):
            cpu = choice(['rock','paper','scissors'])
            player = simpRPS(player)
            result = "**JBB won!**" #assume que o JBB ganha
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
    
    #escolhe entre vários argumentos passados
    @commands.command()
    async def choose(self, *choices : str):
        """Chooses between multiple choices."""
        await self.bot.say(choice(choices))

    #dá resposta positiva ou negativa
    @commands.command()
    async def magicball(self):
        a = ['Most likely', 'Very doubtful', 'Ask again', 'As I see it, yes', 'My sources say no', 'Cannot perdict now', 'Yes', 'Dont count on it', 'Without a doubt', 'Better not tell you']
        await self.bot.say(choice(a))
    
    @commands.command()
    async def asciiass(self):
        a = "⢀⢀⢀⢀⢀⢀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣄⢀⠠⡀\n⢀⢀⢀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣤⣙⣿⣿⣾⣷⣄\n⢀⢀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄\n⢀⢀⠜⣿⠙⣹⡻⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄\n⢀⢀⣰⣿⢠⣿⣇⣶⣿⣿⣿⣿⣿⣿⣿⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢀⢀⢀⢀\n⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢀⢀⠍⠙⢿⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⣴⣾⠃\n⣿⣿⣿⣿⣿⣿⣿⠹⣿⣿⣿⣿⣿⣿⣿⠁⠈⢀⡤⢲⣾⣗⠲⣿⣿⣿⣿⣿⣿⣟⠻⢿⣿⣿⡿⠃\n⡿⣿⣿⣿⣿⣿⣿⡀⢙⣿⣿⣿⣿⣿⣿⢀⠰⠁⢰⣾⣿⣿⡇⢀⣿⣿⣿⣿⣿⣿⡄⠈⢿⣿⣿⣿⣦⣄⡀\n⡇⢻⣿⣿⣿⣿⢿⣇⢀⢀⠙⠷⣍⠛⠛⢀⢀⢀⢀⠙⠋⠉⢀⢀⢸⣿⣿⣿⣿⣿⣷⢀⡟⣿⣿⣿⣿⣿⣟⠦\n⠰⢀⠻⣿⣿⣿⣧⡙⠆⢀⣀⠤⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢸⣿⣿⣿⣿⣿⣿⢿⣧⢸⢻⣿⣿⠿⢿⡆⠁⠠⠠\n⢀⢀⢀⠈⢿⣿⣿⣷⣖⠋⠁⢀⢀⢀⢀⢀⢀⣀⣀⣄⢀⢀⢀⢀⢸⠏⣿⣿⣿⢿⣿⢸⣿⣆⢀⢻⣿⣆⢀⢀⢀⢀⢀⣀⡀\n⢀⢀⢀⢀⠈⣿⣿⣿⣷⡀⢀⢀⢀⢀⢀⡒⠉⠉⢀⢀⢀⢀⢀⢀⢈⣴⣿⣿⡿⢀⡿⢀⢻⣿⣆⡈⣿⣿⠂⢀⢀⢀⢸⣿⢀⢀⢀⢀⢀\n⢀⢀⢀⢀⢀⠘⣿⣿⣿⣷⣄⢀⢀⢀⢀⠐⠄⢀⢀⢀⠈⢀⣀⣴⣿⣿⣿⡿⠁⢀⣡⣶⣿⣿⣿⣿⣿⣯⣄⢀⢀⢀⢸⣿⢀⢀⢀⢀⠐⣠⣾\n⢀⢀⢀⢀⢀⢀⢹⠻⣿⣿⣿⣿⣆⠢⣤⣄⢀⢀⣀⠠⢴⣾⣿⣿⡿⢋⠟⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⡄⣿⣿⢂⠐⢀⣤⡾⡟⠁\n⢀⢀⢀⢀⢀⢀⠸⢀⠘⠿⣿⣿⣿⣦⣹⣿⣀⣀⣀⣀⠘⠛⠋⠁⡀⣄⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢀⣿⣿⣴⣾⣿⣭⣄⢀⢀\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⠛⣽⣿⣿⣿⣿⣿⣿⠁⢀⢀⢀⣡⣾⣿⣿⣿⡟⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢰⣿⣿⣿⣿⣿⣿⣿⣦⣤⣶⣿⡿⢛⢿⡇⠟⠰⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣿⣿⣿⡿⢉⣭⢭⠏⣿⡿⢸⡏⣼⣿⢴⡇⢸⣿⣶⣿⣿⣿⣿⣿⣿⣿⠇⢀⢀⣿⣿⣿⣿⡿⢿⣿⣿⡿⠟⠁\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢰⣿⣿⣿⢃⣶⣶⡏⠸⠟⣱⣿⣧⣛⣣⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠈⢀⢀⡼⠉⠉⠉⠁⢀⢀⢀⢀⢀⢀⢀\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣾⣿⣿⣿⣾⣿⣿⠟⢻⡿⡉⣷⣬⡛⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⢀⢀⠴⠋\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⣸⣿⣿⣿⣿⣿⣿⡿⢰⠘⣰⣇⣿⣿⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⠘⢿⣿⣿⣿⣿⣿⡷⢺⣿⠟⣩⣭⣽⣇⠲⠶⣿⣿⣿⣿⣿⣿⣿⠃\n⢀⢀⢀⢀⢀⢀⢀⢀⠐⢀⣾⣿⣿⣿⣿⠟⢐⡈⣿⣷⣶⠎⣹⡟⠟⣛⣸⣿⣿⣿⣿⣿⣿\n⢀⢀⢀⢀⢀⢀⢀⠠⢀⣼⣿⣿⣿⣿⣯⣼⣿⣷⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⢀⢀⢀⢀⢀⢀⢀⠐⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⢀⢀⢀⢀⢀⢀⢀⢀⠂⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀\n⢀⢀⢀⢀⢀⢀⢀⢀⠈⠼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠹⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠓⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠄⡠⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠉⠛⢦\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⢀⢀⢀⢀⢀⢀⠁⡀\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⠟⠁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠐\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⠙⠻⠿⢿⣿⣿⣿⣿⣿⡿⣿⡟⣿⠹⣮⣿⠁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠠\n⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠉⢀⠛⠳⢾⣷⣾⣿⣹⣿⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢧"
        await self.bot.say(a)
        


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
