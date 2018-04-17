import discord
from discord.ext import commands
from random import randint
import os
from os import path
import json

QUOTES_PATH = './modules/quotes/'

class Quotes():
    
    def __init__(self, bot):
        self.bot = bot
        self.quotes_array = {}
        for f in os.listdir(QUOTES_PATH):
            print(f)
            if path.isfile(path.join(QUOTES_PATH, f)):
                filename, file_ext = path.splitext(f)
                print(filename)
                print(file_ext)
                with open(QUOTES_PATH+f,'r', encoding="utf8") as file:
                    self.quotes_array[filename] = json.load(file)['array']

        
    @commands.command(pass_context=True)
    async def quote(self, ctx):
        await self.bot.say(getRLine(self.quotes_array,'quote'))


    @commands.command(pass_context=True)
    async def quoteA(self, ctx):
        await self.bot.say(getRLine(self.quotes_array, 'quoteA'))


    @commands.command(pass_context=True)
    async def fact(self, ctx):
        await self.bot.say(getRLine(self.quotes_array, 'fact'))


    @commands.command(pass_context=True)
    async def nquoteA(self, ctx):
        await self.bot.say('Existem ' + getNLine(self.quotes_array, 'quoteA') + ' quotes de alunos')


    @commands.command(pass_context=True)
    async def nquote(self, ctx):
        await self.bot.say('Existem ' + getNLine(self.quotes_array, 'quote') + ' quotes do JBB')


    @commands.command(pass_context=True)
    async def nfact(self, ctx):
        await self.bot.say('Existem '+ getNLine(self.quotes_array, 'fact') + ' factos sobre o JBB')


    @commands.command(pass_context=True)
    async def ntotal(self, ctx):
        n = 0
        for array in self.quotes_array.values:
            n += len(array)
        
        await self.bot.say('Existem '+ n + ' frases')

    @commands.command(pass_context=True)
    async def add(self, ctx, file):
        if(ctx.message.author.id == "400031648537640962"):
            print(file)


def getRLine(quotes_array, filename):
    return quotes_array[filename][randint(0, len(quotes_array[filename]) -1 )]

def getNLine(quotes_array, filename):
    return str(len(quotes_array[filename]))

def setup(bot):
    bot.add_cog(Quotes(bot))