from __future__ import print_function
import discord
from discord.ext import commands
import datetime
from apiclient.discovery import build
from aux.check import is_spam
from ftfy import fix_encoding
from googletrans import Translator
from httplib2 import Http
from oauth2client import client, file, tools

#setup the calender API
store = file.Storage('credentials_calendar.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(
            'client_secret.json',
            'https://www.googleapis.com/auth/calendar.readonly')
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


class Google(commands.Cog):
    """Google Apis"""

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

    @commands.command(name='cantina',
                      description="menu of the uminho canteen",
                      brief="menu",
                      aliases=['ementa'])
    @commands.check(is_spam)
    async def cantina(self, ctx ,*, menu='almoço'):
        if menu in self.menus:
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
            value=f"{detector.lang}({round(detector.confidence*100)}%)",
            inline=False)
        embed.add_field(
            name="Translation:",
            value=translation.text,
            inline=True)
        await ctx.send(embed =embed)

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

def setup(bot):
    bot.add_cog(Google(bot))
