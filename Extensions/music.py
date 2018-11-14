import discord
import json
import subprocess
import time
from discord.ext import commands

class Music():
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play',
                      description="play a given music",
                      brief="play a given music",
                      pass_context=True)
    async def play(self, ctx, music):
    #play a mp3 file
        #check if user in voice channel
        if ctx.message.author.voice_channel:
            music = music.lower()
            #check if requested music exists
            if music in self.bot.musicMap:
                #if bot is not connected to voice channel connect
                if self.bot.voice_client == None:
                   voice = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
                   self.bot.voice_client = voice
                #if bot is connected and is playing dont play
                if self.bot.player_client != None and self.bot.player_client.is_playing():
                    await self.bot.say("Already Playing")
                else:
                    #create player and play file
                    player = self.bot.voice_client.create_ffmpeg_player(self.bot.MUSIC_PATH + self.bot.musicMap[music])
                    self.bot.player_client = player
                    player.start()
            else:
                await self.bot.say("Invalid Music")
        else:
            await self.bot.say("You're not in a voice channel")
    
    @commands.command(name='stop',
                      description="stop music and leave voice channel",
                      brief="stop music",
                      pass_context=True)
    async def stop(self, ctx):
        #check if user in voice channel
        if ctx.message.author.voice_channel:
            #cheack if bot in voice channel
            if self.bot.voice_client:
                #disconnect
                await self.bot.voice_client.disconnect()
                self.bot.voice_client = None
                self.bot.player_client = None
            else:
                await self.bot.say("JBB not in a voice channel")
        else:
            await self.bot.say("You're not in a voice channel")

def setup(bot):
    bot.add_cog(Music(bot))
