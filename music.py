import discord
from baseconvert import base
from discord.ext import commands
from random import randint
import 

class Programming():
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    def play(self, ctx, query):
            """Plays a file from the local filesystem"""
    
            if ctx.voice_client is None:
                if ctx.author.voice.channel:
                    await ctx.author.voice.channel.connect()
                else:
                    return await self.bot.send("Not connected to a voice channel.")
    
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
    
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./Music/' + query))
            ctx.voice_client.play(source, after=lambda e: print(
                'Player error: %s' % e) if e else None)
    
            await self.bot.send('Now playing: {}'.format(query)) 


def setup(bot):
    bot.add_cog(Music(bot))