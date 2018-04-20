import discord
from discord.ext import commands
import random
from random import randint
import os
from os import path
import json

QUOTES_PATH = './modules/quotes/'

class Quotes():
    
    def __init__(self, bot):
        self.bot = bot
        self.quotes_dict = {}
        for f in os.listdir(QUOTES_PATH):
            if path.isfile(path.join(QUOTES_PATH, f)):
                filename, file_ext = path.splitext(f)
                with open(QUOTES_PATH + f, 'r', encoding="utf8") as file:
                    self.quotes_dict[filename] = json.load(file)['array']

        
    @commands.command(pass_context=True)
    async def quote(self, ctx):
        await self.bot.say(getRLine(self.quotes_dict,'quote'))


    @commands.command(pass_context=True)
    async def quoteA(self, ctx):
        await self.bot.say(getRLine(self.quotes_dict, 'quoteA'))


    @commands.command(pass_context=True)
    async def fact(self, ctx):
        await self.bot.say(getRLine(self.quotes_dict, 'fact'))


    @commands.command(pass_context=True)
    async def nquoteA(self, ctx):
        await self.bot.say('Existem ' + getNLine(self.quotes_dict, 'quoteA') + ' quotes de alunos')


    @commands.command(pass_context=True)
    async def nquote(self, ctx):
        await self.bot.say('Existem ' + getNLine(self.quotes_dict, 'quote') + ' quotes do JBB')


    @commands.command(pass_context=True)
    async def nfact(self, ctx):
        await self.bot.say('Existem '+ getNLine(self.quotes_dict, 'fact') + ' factos sobre o JBB')


    @commands.command(pass_context=True)
    async def ntotal(self, ctx):
        n =  int(getNLine(self.quotes_dict, 'quoteA'))
        n += int(getNLine(self.quotes_dict, 'quote'))
        n += int(getNLine(self.quotes_dict, 'fact'))
        n += int(getNLine(self.quotes_dict, 'quoteAdmin'))
        
        await self.bot.say('Existem '+ str(n) + ' frases')


    @commands.command(pass_context=True)
    async def quoteAdmin(self, ctx):
        if "Administrador" in [y.name for y in ctx.message.author.roles]:
            await self.bot.say(getRLine(self.quotes_dict, 'quoteAdmin'))
        else:
            await self.bot.say('Invalid user')


    @commands.command(pass_context=True)
    async def nquoteAdmin(self, ctx):
        if "Administrador" in [y.name for y in ctx.message.author.roles]:
            await self.bot.say('Existem '+ getNLine(self.quotes_dict, 'quoteAdmin') + ' quotes de Admin')
        else:
            await self.bot.say('Invalid user')
        

    @commands.command(pass_context=True)
    async def add(self, ctx, file, quote):
        if ctx.message.author == discord.AppInfo.owner:
            await self.bot.say('Invalid user')

        elif file not in self.quotes_dict:
            await self.bot.say('Invalid category')

        elif len(quote) < 1:
            await self.bot.say('Invalid quote')

        else:
            self.quotes_dict[file].append(quote)
            updateQuotes(self.quotes_dict, file)
            await self.bot.say('quote "'+ quote +'" added to file `'+ file +'`')



def getRLine(quotes_dict, filename):
    return random.choice(quotes_dict[filename])


def getNLine(quotes_dict, filename):
    return str(len(quotes_dict[filename]))


def updateQuotes(quotes_dict, filename):
    with open(QUOTES_PATH + filename + '.json', 'w', encoding='utf8') as file:
        d = {'array': quotes_dict[filename]}
        json.dump(d, file, indent=4)


def setup(bot):
    bot.add_cog(Quotes(bot))