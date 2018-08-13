import discord
import json
import subprocess
import time
from discord.ext import commands

class Music():
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def play(self, ctx, music):
        if ctx.message.author.voice_channel:
            music = music.lower()
            if music in self.bot.musicMap:
                if self.bot.voice_client == None:
                   voice = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
                   self.bot.voice_client = voice
                if self.bot.player_client != None and self.bot.player_client.is_playing():
                    await self.bot.say("Already Playing")
                else:
                    player = self.bot.voice_client.create_ffmpeg_player(self.bot.MUSIC_PATH + self.bot.musicMap[music])
                    self.bot.player_client = player
                    player.start()
            else:
                await self.bot.say("Invalid Music")
        else:
            await self.bot.say("You're not in a voice channel")
    
    @commands.command(pass_context=True)
    async def stop(self, ctx):
        if ctx.message.author.voice_channel:
            if self.bot.voice_client:
                await self.bot.voice_client.disconnect()
                self.bot.voice_client = None
                self.bot.player_client = None
            else:
                await self.bot.say("JBB not in a voice channel")
        else:
            await self.bot.say("You're not in a voice channel")

def setup(bot):
    bot.add_cog(Music(bot))
