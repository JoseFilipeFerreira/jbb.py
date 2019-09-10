import discord
from discord.ext import commands
import random
import os
import json
from os import path
from fuzzywuzzy import fuzz, process
from random import randint, shuffle

class Quotes():

    def __init__(self, bot):
        self.bot = bot
        self.quotes_dict = {}
        for f in os.listdir(bot.QUOTES_PATH):
            if path.isfile(path.join(bot.QUOTES_PATH, f)):
                filename, _ = path.splitext(f)
                with open(bot.QUOTES_PATH + f, 'r', encoding="utf8") as file:
                    self.quotes_dict[filename] = json.load(file)['array']

    @commands.command(name='quote',
                      description="random quote from JBB",
                      brief="quote from JBB",
                      pass_context=True)
    async def quote(self, ctx):
        await self.bot.say(getRLine(self.quotes_dict,'quote'))

    @commands.command(name='quoteA',
                      description="random quote from Students",
                      brief="quote from Students",
                      pass_context=True)
    async def quoteA(self, ctx):
        l = getRLine(self.quotes_dict, 'quoteA')
        await self.bot.say("{} - {}".format(l["content"], l["name"]))
    
    @commands.command(name='quoteP',
                      description="random quote from Teachers",
                      brief="quote from Teachers",
                      pass_context=True)
    async def quoteP(self, ctx):
        await self.bot.say(getRLine(self.quotes_dict, 'quoteP'))

    @commands.command(name='fact',
                      description="random fact of JBB",
                      brief="fact of JBB",
                      pass_context=True)
    async def fact(self, ctx):
        await self.bot.say(getRLine(self.quotes_dict, 'fact'))

    @commands.command(name='dadjoke',
                      description="random dad joke",
                      brief="random dad joke",
                      pass_context=True)
    async def dadjoke(self, ctx):
        await self.bot.say(getRLine(self.quotes_dict, 'dadjoke'))

    @commands.command(name='nquoteA',
                      description="number of student quotes",
                      brief="number of student quotes",
                      pass_context=True)
    async def nquoteA(self, ctx):
        await self.bot.say('Existem ' + getNLine(self.quotes_dict, 'quoteA') + ' quotes de alunos')

    @commands.command(name='nquote',
                      description="number of JBB quotes",
                      brief="number of JBB quotes",
                      pass_context=True)
    async def nquote(self, ctx):
        await self.bot.say('Existem ' + getNLine(self.quotes_dict, 'quote') + ' quotes do JBB')
    
    @commands.command(name='nquoteP',
                      description="number of teachers quotes",
                      brief="number of teachers quotes",
                      pass_context=True)
    async def nquoteP(self, ctx):
        await self.bot.say('Existem ' + getNLine(self.quotes_dict, 'quoteP') + ' quotes do Professores')


    @commands.command(name='nfact',
                      description="number of JBB facts",
                      brief="number of JBB facts",
                      pass_context=True)
    async def nfact(self, ctx):
        await self.bot.say('Existem '+ getNLine(self.quotes_dict, 'fact') + ' factos sobre o JBB')

    @commands.command(name='ndadjoke',
                      description="number of dadjokes",
                      brief="number of dadjokes",
                      pass_context=True)
    async def ndadjoke(self, ctx):
        await self.bot.say('Existem '+ getNLine(self.quotes_dict, 'dadjoke') + ' dad jokes')


    @commands.command(name='ntotal',
                      description="total number of quotes",
                      brief="total number of quotes",
                      pass_context=True)
    async def ntotal(self, ctx):
        n =  int(getNLine(self.quotes_dict, 'quoteA'))
        n += int(getNLine(self.quotes_dict, 'quoteP'))
        n += int(getNLine(self.quotes_dict, 'quote'))
        n += int(getNLine(self.quotes_dict, 'fact'))
        n += int(getNLine(self.quotes_dict, 'dadjoke'))

        await self.bot.say('Existem '+ str(n) + ' frases')

    @commands.command(name='add',
                      description="add a quote [OWNER ONLY]",
                      brief="add a quote",
                      pass_context=True)
    async def add(self, ctx, file,*, quote):
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
            updateQuotes(self, self.quotes_dict, file)
            await self.bot.say('quote "'+ quote +'" added to file `'+ file +'`')
    
    @commands.command(name='remove',
                      description="remove a quote [OWNER ONLY]",
                      brief="remove a quote",
                      aliases=['delete'],
                      pass_context=True)
    async def remove(self, ctx, file):
        appInfo = await self.bot.application_info()
        owner = appInfo.owner
        #TODO optimize one day
        if ctx.message.author != owner:
            await self.bot.say('Invalid user')

        elif file not in self.quotes_dict:
            await self.bot.say('Invalid category')

        else:
            quote = self.quotes_dict[file].pop()
            updateQuotes(self, self.quotes_dict, file)
            await self.bot.say('quote "'+ quote +'" removed from file `'+ file +'`')

    @commands.command(name='quoteS',
                      description="search a quote using fuzzy search",
                      brief="search a quote",
                      aliases=['grep'],
                      pass_context=True)
    async def quoteS(self, ctx, *, search):
    #search a quote using fuzzysearching
        quoteA = list(map(
            lambda x: "{} - {}".format(x["content"], x["name"]),
            self.quotes_dict['quoteA']))
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


def updateQuotes(self, quotes_dict, filename):
#update a JSON file
    with open(self.bot.QUOTES_PATH + filename + '.json', 'w', encoding='utf8') as file:
        d = {'array': quotes_dict[filename]}
        json.dump(d, file, indent=4)


def setup(bot):
    bot.add_cog(Quotes(bot))
