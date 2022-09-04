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
        if args:
            u = []
            if args.lower() == "me":
                for q in self.quotes_dict['quoteA']:
                    if q['id'] == ctx.message.author.id:
                        u.append(q)
                if len(u) == 0:
                    await ctx.send("You don't have a quote")
                    return
                l = choice(u)

            elif args.lower() == "nos":
                last_users = set(())
                async for msg in ctx.channel.history(limit=100):
                    last_users.add(msg.author.id)
                    if len(last_users) == 10:
                        break
                while len(u) == 0 or len(last_users) != 0:
                    chosen_user = choice(tuple(last_users))
                    last_users.discard(chosen_user)
                    for q in self.quotes_dict['quoteA']:
                        if q['id'] == chosen_user:
                            u.append(q)
                if len(u) == 0:
                    await ctx.send("No quote can be found")
                    return
                l = choice(u)

        s = "{} - {}".format(l["content"], l["name"])
        if "<@!" in s:
            message_sent = await ctx.send(discord.utils.escape_mentions(s))
            await message_sent.edit(s)
        else:
            await ctx.send(s)

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
    async def nquoteA(self, ctx, args=None):
        if args and args.lower() =="me":
            u = 0
            for q in self.quotes_dict['quoteA']:
                if q['id'] == ctx.message.author.id:
                    u += 1
            if u == 0:
                await ctx.send("You don't have a quote")
            else:
                await ctx.send(f"You have {u} quotes")
        else:
            await ctx.send('Existem ' + getNLine(self.quotes_dict, 'quoteA') + ' quotes de alunos')

    @commands.command(name='quoteRank',
                      description="Ranking of student quotes",
                      brief="Ranking of student quotes")
    async def quoteRank(self, ctx, args=None):
        embed = discord.Embed(
            title = 'Quote Whores do DI',
            color=self.bot.embed_color)
        quote_ids = list(map(lambda q: q['id'], self.quotes_dict['quoteA']))
        nquotes = []
        for id in set(quote_ids):
            nquotes.append({
                "id": id,
                "nquotes": quote_ids.count(id)})

        nquotes.sort(key=lambda n: n["nquotes"], reverse=True)

        for i in range(3):
            quotes = nquotes[i]
            member = ctx.message.guild.get_member(quotes["id"])

            embed.add_field(
                name="{0}. {1}".format(i + 1, member.display_name),
                value="Quotes: {0}".format(quotes["nquotes"]),
                inline=False)

        await ctx.send(embed=embed)

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

        s = result[0][0]

        if "<@!" in s:
            message_sent = await ctx.send(discord.utils.escape_mentions(s))
            await message_sent.edit(s)
        else:
            await ctx.send(s)

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
