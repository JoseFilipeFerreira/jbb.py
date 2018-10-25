import discord
from discord.ext import commands
import random
from random import randint
from random import shuffle
import os
from os import path
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
    #gives a quote from JBB
        await self.bot.say(getRLine(self.quotes_dict,'quote'), tts=True)


    @commands.command(pass_context=True)
    async def quoteA(self, ctx):
    #gives a quote from Students
        await self.bot.say(getRLine(self.quotes_dict, 'quoteA'), tts=True)
    
    @commands.command(pass_context=True)
    async def quoteP(self, ctx):
    #gives a quote from teachers
        await self.bot.say(getRLine(self.quotes_dict, 'quoteP'), tts=True)


    @commands.command(pass_context=True)
    async def fact(self, ctx):
    #gives a true fact of JBB
        await self.bot.say(getRLine(self.quotes_dict, 'fact'), tts=True)

    @commands.command(pass_context=True)
    async def dadjoke(self, ctx):
    #gives a dad joke
        await self.bot.say(getRLine(self.quotes_dict, 'dadjoke'), tts=True)


    @commands.command(pass_context=True)
    async def nquoteA(self, ctx):
    #number of student quotes
        await self.bot.say('Existem ' + getNLine(self.quotes_dict, 'quoteA') + ' quotes de alunos')


    @commands.command(pass_context=True)
    async def nquote(self, ctx):
    #number of JBB quotes
        await self.bot.say('Existem ' + getNLine(self.quotes_dict, 'quote') + ' quotes do JBB')
    
    @commands.command(pass_context=True)
    async def nquoteP(self, ctx):
    #number of teachers quotes
        await self.bot.say('Existem ' + getNLine(self.quotes_dict, 'quoteP') + ' quotes do Professores')


    @commands.command(pass_context=True)
    async def nfact(self, ctx):
    #number of JBB facts
        await self.bot.say('Existem '+ getNLine(self.quotes_dict, 'fact') + ' factos sobre o JBB')

    @commands.command(pass_context=True)
    async def ndadjoke(self, ctx):
    #number of dadjokes
        await self.bot.say('Existem '+ getNLine(self.quotes_dict, 'dadjoke') + ' dad jokes')


    @commands.command(pass_context=True)
    async def ntotal(self, ctx):
    #total number of quotes
        n =  int(getNLine(self.quotes_dict, 'quoteA'))
        n += int(getNLine(self.quotes_dict, 'quoteP'))
        n += int(getNLine(self.quotes_dict, 'quote'))
        n += int(getNLine(self.quotes_dict, 'fact'))
        n += int(getNLine(self.quotes_dict, 'quoteAdmin'))
        n += int(getNLine(self.quotes_dict, 'dadjoke'))

        await self.bot.say('Existem '+ str(n) + ' frases')


    @commands.command(pass_context=True)
    async def quoteAdmin(self, ctx):
    #gives a quote from admins
        if "Administrador" in [y.name for y in ctx.message.author.roles]:
            await self.bot.say(getRLine(self.quotes_dict, 'quoteAdmin'))
        else:
            await self.bot.say('Invalid user')


    @commands.command(pass_context=True)
    async def nquoteAdmin(self, ctx):
    #number of admin quotes
        if "Administrador" in [y.name for y in ctx.message.author.roles]:
            await self.bot.say('Existem '+ getNLine(self.quotes_dict, 'quoteAdmin') + ' quotes de Admin')
        else:
            await self.bot.say('Invalid user')


    @commands.command(pass_context=True)
    async def add(self, ctx, file,*, quote):
    #add a quote
        appInfo = await self.bot.application_info()
        owner = appInfo.owner
        #TODO optimize one day
        if ctx.message.author != owner:
            await self.bot.say('Invalid user')

        elif file not in self.quotes_dict:
            await self.bot.say('Invalid category')

        elif len(quote) < 1:
            await self.bot.say('Invalid quote')

        else:
            self.quotes_dict[file].append(quote)
            updateQuotes(self.quotes_dict, file)
            await self.bot.say('quote "'+ quote +'" added to file `'+ file +'`')
    
    @commands.command(pass_context=True)
    async def remove(self, ctx, file):
    #remove a quote
        appInfo = await self.bot.application_info()
        owner = appInfo.owner
        #TODO optimize one day
        if ctx.message.author != owner:
            await self.bot.say('Invalid user')

        elif file not in self.quotes_dict:
            await self.bot.say('Invalid category')

        else:
            quote = self.quotes_dict[file].pop()
            updateQuotes(self.quotes_dict, file)
            await self.bot.say('quote "'+ quote +'" removed from file `'+ file +'`')

    @commands.command(pass_context=True)
    async def quoteS(self, ctx, *, search):
    #search a quote using fuzzysearching
        quoteA = self.quotes_dict['quoteA']
        quote = self.quotes_dict['quote']
        fact = self.quotes_dict['fact'] 
        candidates = quoteA + quote + fact
        random.shuffle(candidates)
        
        result = process.extract(search, candidates, limit=1)

        await self.bot.say(result[0][0])

def getRLine(quotes_dict, filename):
#get a random quote
    return random.choice(quotes_dict[filename])


def getNLine(quotes_dict, filename):
#get number of quotes
    return str(len(quotes_dict[filename]))


def updateQuotes(quotes_dict, filename):
#update a JSON file
    with open(QUOTES_PATH + filename + '.json', 'w', encoding='utf8') as file:
        d = {'array': quotes_dict[filename]}
        json.dump(d, file, indent=4)


def setup(bot):
    bot.add_cog(Quotes(bot))
