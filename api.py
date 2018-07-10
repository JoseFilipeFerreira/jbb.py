from __future__ import print_function
import discord
import wolframalpha
from baseconvert import base
from discord.ext import commands
from random import randint
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from googletrans import Translator
import urbandictionary as ud

#setup the calender API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


client = wolframalpha.Client(open('WA_KEY').readline().rstrip())

class Api():
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def ask(self, ctx):
        query = ctx.message.content[5:]
        res = client.query(query)
        if res['@success'] == 'false':
            strRes = "Couldn't find an answer"
        else:
            strRes = next(res.results).text
            
        answer = '**' + query +'**' + '\n```' + strRes + '```'
        await self.bot.say(answer)

    @commands.command(pass_context=True)
    async def cantina(self, ctx):
        #call calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId = 'primary',
            timeMin = now,
            maxResults = 3,
            singleEvents = True,
            orderBy = 'startTime').execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcomig events found')

        embed = discord.Embed(title="Ementa da Cantina", color=0xfbfb00)
            
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            arrayDate = start.split('T')[0].split('-')
            embed.add_field(
                name = arrayDate[2] + '-' + arrayDate[1] + '-' + arrayDate[0],
                value = event['summary'],
                inline=False)

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def translate(self, ctx, *query):
        query = ' '.join(word for word in query)
        translator = Translator()
        translation = translator.translate(query, dest='pt')
        detector = translator.detect(query)
        embed = discord.Embed(title="Translating to PT:", description=query, color=0xfbfb00)
        embed.set_thumbnail(url = "http://logonoid.com/images/google-translate-logo.png")
        embed.add_field(name="Detected Language:", value="{0}({1}%)".format(detector.lang, round(detector.confidence*100)), inline=False)
        embed.add_field(name="Translation:", value=translation.text, inline=True)
        await self.bot.say(embed =embed)

    @commands.command(pass_context=True)
    async def urban(self, ctx, *query):
        query = ' '.join(word for word in query)
        defs = ud.define(query)
        d = defs[0]
        embed = discord.Embed(title="Definition of {}".format(query), description=d.definition, color=0xfbfb00)
        embed.set_thumbnail(url = "http://campbelllawobserver.com/wp-content/uploads/2014/03/Urban-Dictionary-e1372286057646.png")
        embed.add_field(name="Example", value=d.example, inline=False)
        embed.add_field(name=":thumbsup:", value=d.upvotes, inline=True)
        embed.add_field(name=":thumbsdown:", value=d.downvotes, inline=True)
        await self.bot.say(embed =embed)
        
def setup(bot):
    bot.add_cog(Api(bot))