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
storing = file.Storage('credentialsy.json')
credss = storing.get()
if not credss or credss.invalid:
    flower = client.flow_from_clientsecrets('client_secret.json', YOUTUBE_READONLY_SCOPE)
    credss = tools.run_flow(flower, storing)
youtube = build('youtube', 'v3', http=credss.authorize(Http()))

class Youtube():
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='videos', pass_context=True)
    async def videos(self):
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

        

#NO LONGER AVAILABLE
#def getVideos():
#    foundAll = False
#    ind = 1
#    videos = []
#    while not foundAll:
#        inp = urllib.request.urlopen('http://gdata.youtube.com/feeds/api/videos?start-index=0&max-results=50&alt=json&orderby=published&author=JBB [BOT]')
#        try:
#            resp = json.load(inp)
#            inp.close()
#            returnedVideos = resp['feed']['entry']
#            for video in returnedVideos:
#                videos.append( video ) 
#    
#            ind += 50
#            print(len(videos))
#            if (len(returnedVideos)< 50):
#                foundAll = True
#        except:
#            #catch the case where the number of videos in the channel is a multiple of 50
#            print("error")
#            foundAll = True
#    
#    for video in videos:
#        print(video['title']) # video title
#        print(video['link'][0]['href']) #url

def setup(bot):
    bot.add_cog(Youtube(bot))
