from __future__ import print_function
import discord
from discord.ext import commands
import aiohttp
import datetime
import wolframalpha
from apiclient.discovery import build
from ftfy import fix_encoding
from googletrans import Translator
from httplib2 import Http
from oauth2client import client, file, tools

#setup the calender API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('credentials_calendar.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

#setup wolframalpha API
client = wolframalpha.Client(open('WA_KEY').readline().rstrip())

class Api(commands.Cog):
    """Conjunto de APIs"""
    
    def __init__(self, bot):
        self.bot = bot
        self.menus = {
            "almoço": "almoço",
            "jantar": "jantar",
            "almoço veg": "almoço vegetariano",
            "almoço vegetariano": "almoço vegetariano",
            "vegetariano": "almoço vegetariano",
            "veg": "almoço vegetariano",
            "jantar veg": "jantar vegetariano",
            "jantar vegetariano": "jantar vegetariano"}

    @commands.command(name='ask',
                      description="replies to a query with the short text answer of the wolfram alpha API",
                      brief="wolfram alpha API")
    async def ask(self, ctx, *, query):
        res = client.query(query)
        if res['@success'] == 'false':
            strRes = "Couldn't find an answer"
        else:
            strRes = next(res.results).text
        await ctx.send('**' + query +'**' + '\n```' + strRes + '```')

    @commands.command(name='cantina',
                      description="menu of the uminho canteen",
                      brief="menu",
                      aliases=['ementa'])
    async def cantina(self, ctx ,*, menu=None):
        if not menu:
            calendar_name = 'almoço'
        elif menu in self.menus:
            menu = menu.lower()
            calendar_name = self.menus[menu]
        else:
            await ctx.send("Menu Inválido")
            return
        
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId = get_calendar_ids()[calendar_name],
            timeMin = now,
            maxResults = 3,
            singleEvents = True,
            orderBy = 'startTime').execute()

        embed = discord.Embed(
            title="Ementa da Cantina",
            description=calendar_name,
            color=self.bot.embed_color)

        for event in events_result.get('items', []):
            arrayDate = event['start'].get('dateTime', event['start'].get('date')).split('T')[0].split('-')
            embed.add_field(
                name = arrayDate[2] + '-' + arrayDate[1] + '-' + arrayDate[0],
                # podia dar fix, só que não
                # value = fix_encoding(event['summary']),
                value = event['summary'],
                inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='translate',
                      description="translate a given query to portuguese",
                      brief="translate to PT")
    async def translate(self, ctx, *, query):
        translator = Translator()
        translation = translator.translate(query, dest='pt')
        detector = translator.detect(query)
        embed = discord.Embed(title="Translating to PT:", description=query, color=0xfbfb00)
        embed.set_thumbnail(url = "http://logonoid.com/images/google-translate-logo.png")
        embed.add_field(
            name="Detected Language:",
            value="{0}({1}%)".format(detector.lang, round(detector.confidence*100)),
            inline=False)
        embed.add_field(
            name="Translation:",
            value=translation.text,
            inline=True)
        await ctx.send(embed =embed)

    @commands.command(name='urban',
                      description="Get a urban defenition of a query",
                      brief="search urban")
    async def urban(self, ctx, * query : str):
        search_terms = "+".join(query)
        url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    result = await response.json()
            if result["list"]:
                top_def = result['list'][0]

                embed = discord.Embed(
                    title="Definition of {}".format(top_def['word']),
                    url=top_def['permalink'],
                    description=top_def['definition'],
                    color=self.bot.embed_color)
                
                embed.set_thumbnail(
                    url = "http://campbelllawobserver.com/wp-content/uploads/2014/03/Urban-Dictionary-e1372286057646.png")

                embed.add_field(
                    name="Example",
                    value=top_def['example'],
                    inline=False)
                embed.add_field(
                    name=":thumbsup:",
                    value=top_def['thumbs_up'],
                    inline=True)
                embed.add_field(
                    name=":thumbsdown:",
                    value=top_def['thumbs_down'],
                    inline=True)
                
                embed.set_footer(
                    text="Submited by {}".format(top_def['author']))
                await ctx.send(embed =embed)
            else:
                await ctx.send("Your query gave no results.")
        except:
            await self.bot.say("Something unexpected went wrong.")   

def setup(bot):
    bot.add_cog(Api(bot))

def get_calendar_ids():
#return all added extenal calendars in a dict
#with calendar name as key and calendar id as value
    page_token = None
    calendar_ids = {}
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if '@group.calendar.google.com' in calendar_list_entry['id']:
                key = calendar_list_entry['summary']
                if 'summaryOverride' in calendar_list_entry:
                   key = calendar_list_entry['summaryOverride']
                calendar_ids[key] = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    return calendar_ids
