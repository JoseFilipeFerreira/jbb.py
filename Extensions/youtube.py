import discord
import urllib.request
import json
from discord.ext import commands
from random import choice

author = 'JBB [BOT]'

class Youtube():
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='video',
                      description="top kek o youtube eliminou isto",
                      brief="random url for yotube video",
                      pass_context=True)
    async def video(self, ctx):
    #top kek já deu
        print("Top kek não dá")
        

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
