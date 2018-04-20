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
<<<<<<< HEAD
=======
            nomesN = nomesN + 1
>>>>>>> ed0d8442b42991d9753c81713c96b1bcd38dc5b9

        await self.bot.say(embed=embed)
        



def setup(bot):
    bot.add_cog(Api(bot))
