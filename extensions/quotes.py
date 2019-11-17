import discord
from discord.ext import commands
import json
from fuzzywuzzy import fuzz, process
from random import choice, shuffle

class Quotes(commands.Cog):
    """All quotes stored"""
    def __init__(self, bot):
        self.bot = bot
        self.quotes_dict = json.load(open(bot.QUOTES_PATH, 'r', encoding="utf8"))

    @commands.command(name='quote',
                      description="random quote from JBB",
                      brief="quote from JBB")
    async def quote(self, ctx):
        await ctx.send(getRLine(self.quotes_dict,'quote'))

    @commands.command(name='quoteA',
                      brief="quote from Students")
    async def quoteA(self, ctx, args = None):
        """random quote from Students"""
        l = getRLine(self.quotes_dict, 'quoteA')
        if args and args.lower() == "me":
            u = []
            for q in self.quotes_dict['quoteA']:
                if q['id'] == ctx.message.author.id:
                    u.append(q)
            if len(u) == 0:
                await ctx.send("You don't have a quote")
                return
            l = choice(u)
        await ctx.send("{} - {}".format(l["content"], l["name"]))


    
    @commands.command(name='quoteP',
                      description="random quote from Teachers",
                      brief="quote from Teachers")
    async def quoteP(self, ctx):
        await ctx.send(getRLine(self.quotes_dict, 'quoteP'))

    @commands.command(name='fact',
                      description="random fact of JBB",
                      brief="fact of JBB")
    async def fact(self, ctx):
        await ctx.send(getRLine(self.quotes_dict, 'fact'))

    @commands.command(name='dadjoke',
                      description="random dad joke",
                      brief="random dad joke")
    async def dadjoke(self, ctx):
        await ctx.send(getRLine(self.quotes_dict, 'dadjoke'))

    @commands.command(name='nquoteA',
                      description="number of student quotes",
                      brief="number of student quotes")
    async def nquoteA(self, ctx):
        await ctx.send('Existem ' + getNLine(self.quotes_dict, 'quoteA') + ' quotes de alunos')

    @commands.command(name='nquote',
                      description="number of JBB quotes",
                      brief="number of JBB quotes")
    async def nquote(self, ctx):
        await ctx.send('Existem ' + getNLine(self.quotes_dict, 'quote') + ' quotes do JBB')
    
    @commands.command(name='nquoteP',
                      description="number of teachers quotes",
                      brief="number of teachers quotes")
    async def nquoteP(self, ctx):
        await ctx.send('Existem ' + getNLine(self.quotes_dict, 'quoteP') + ' quotes do Professores')


    @commands.command(name='nfact',
                      description="number of JBB facts",
                      brief="number of JBB facts")
    async def nfact(self, ctx):
        await ctx.send('Existem '+ getNLine(self.quotes_dict, 'fact') + ' factos sobre o JBB')

    @commands.command(name='ndadjoke',
                      description="number of dadjokes",
                      brief="number of dadjokes")
    async def ndadjoke(self, ctx):
        await ctx.send('Existem '+ getNLine(self.quotes_dict, 'dadjoke') + ' dad jokes')


    @commands.command(name='ntotal',
                      description="total number of quotes",
                      brief="total number of quotes")
    async def ntotal(self, ctx):
        n = 0
        for k in self.quotes_dict.keys():
            n += int(getNLine(self.quotes_dict, k))

        await ctx.send('Existem '+ str(n) + ' frases')

    @commands.command(name='add',
                      description="add a quote [OWNER ONLY]",
                      brief="add a quote")
    @commands.is_owner()
    async def add(self, ctx, cat,*, msgs):
        if cat not in self.quotes_dict:
            await ctx.send('Invalid category')
            return
        if len(msgs) < 1:
            await ctx.send('Invalid quote')
            return
        if cat == "quoteA":
            msgArr = msgs.strip().split()
            try:
                msgArr = list(map(lambda x: int(x) ,msgArr))
                tmp = []
                for msgID in msgArr:
                    tmp.append(await ctx.fetch_message(msgID))
                msgArr = tmp
            except:
                await ctx.send("Invalid Messages IDs")
                return
            content = "\n".join(list(map(lambda x: x.content,msgArr)))
            
            name = msgArr[0].author.display_name
            self.quotes_dict[cat].append({
                "content": content,
                "name": name,
                "id": msgArr[0].author.id})
            newQ = "{} - {}".format(content, name) 
        else:
            self.quotes_dict[cat].append(msgs)
            newQ = msgs 

        updateQuotes(self)
        await ctx.send('quote "'+ newQ +'" added to `'+ cat +'`')
    
    @commands.command(name='remove',
                      description="remove a quote [OWNER ONLY]",
                      brief="remove a quote",
                      aliases=['delete'])
    @commands.is_owner()
    async def remove(self, ctx, cat):
        if cat not in self.quotes_dict:
            await ctx.send('Invalid category')
        else:
            quote = self.quotes_dict[cat].pop()
            updateQuotes(self)
            await ctx.send('quote "'+ str(quote) +'" removed from `'+ cat +'`')

    @commands.command(name='quoteS',
                      description="search a quote using fuzzy search",
                      brief="search a quote",
                      aliases=['grep'])
    async def quoteS(self, ctx, *, search):
    #search a quote using fuzzysearching
        quoteA = list(map(
            lambda x: "{} - {}".format(x["content"], x["name"]),
            self.quotes_dict['quoteA']))
        quote = self.quotes_dict['quote']
        fact = self.quotes_dict['fact'] 
        candidates = quoteA + quote + fact
        shuffle(candidates)
        
        result = process.extract(search, candidates, limit=1)

        await ctx.send(result[0][0])

def getRLine(quotes_dict, filename):
#get a random quote
    return choice(quotes_dict[filename])


def getNLine(quotes_dict, filename):
#get number of quotes
    return str(len(quotes_dict[filename]))


def updateQuotes(self):
#update a JSON file
    with open(self.bot.QUOTES_PATH, 'w', encoding='utf8') as file:
        json.dump(self.quotes_dict, file, indent=4)

def setup(bot):
    bot.add_cog(Quotes(bot))
