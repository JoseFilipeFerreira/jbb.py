import discord
import json
import subprocess
from mcstatus import MinecraftServer
from discord.ext import commands

class Minecraft():
    def __init__(self, bot):
        self.bot = bot
        self.ip = "178.33.27.52:25586"

    @commands.command(name='mcstatus',
                      description="minecraft server satus",
                      brief="minecraft server satus",
                      pass_context=True)
    async def mcstatus(self, ctx):

        server = MinecraftServer.lookup(self.ip)
        status = server.status()

        embed = discord.Embed(
            title = 'Minecraft Server',
            description=status.description["text"],
            color=self.bot.embed_color
        )

        embed.add_field(
            name='IP',
            value=self.ip,
            inline=False)
        
        embed.add_field(
            name='Online Users',
            value="{0}/{1}".format(status.players.online, status.players.max),
            inline=False)
        
        embed.add_field(
            name='Version',
            value=status.version.name,
            inline=False)
        
        embed.add_field(
            name='Ping',
            value="{} ms".format(status.latency),
            inline=False)
        
        embed.set_thumbnail(url=ctx.message.server.icon_url)
         
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Minecraft(bot))
