import discord
import urllib.request
import json
from discord.ext import commands
from random import choice
from oauth2client import file, client, tools
from apiclient.discovery import build
from httplib2 import Http

author = 'JBB [BOT]'

YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
storing = file.Storage('credentials_youtube.json')
credss = storing.get()
if not credss or credss.invalid:
    flower = client.flow_from_clientsecrets('client_secret.json', YOUTUBE_READONLY_SCOPE)
    credss = tools.run_flow(flower, storing)
youtube = build('youtube', 'v3', http=credss.authorize(Http()))

class Youtube():
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='videos',
        description="send random video from the bot youtube channel",
        brief="random Youtube video",
        pass_context=True)
    async def videos(self, ctx):
        channels_response = youtube.channels().list(mine=True, part="contentDetails").execute()
        for channel in channels_response["items"]:
            # From the API response, extract the playlist ID that identifies the list
            # of videos uploaded to the authenticated user's channel.
            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=uploads_list_id,
            part="snippet",
            maxResults=50
        )
        playlistitems_list_response = playlistitems_list_request.execute()

        # Print information about each video.
        #for playlist_item in playlistitems_list_response["items"]:
        playlist_item = choice(playlistitems_list_response["items"])
        title = playlist_item["snippet"]["title"]
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        await self.bot.say("http://youtube.com/watch?v=%s" % (video_id))

def setup(bot):
    bot.add_cog(Youtube(bot))
