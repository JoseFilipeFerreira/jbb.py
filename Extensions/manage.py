import discord
import json
import os
import time
import subprocess
from discord.ext import commands

class Manage(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='update',
                      description="update the code from github and reboot [OWNER ONLY]",
                      brief="update the bot")
    @commands.is_owner()
    async def update(self, ctx):
        await self.bot.change_presence(game=discord.Game(name='rebooting'))
        subprocess.call("./update.sh")
    

    @commands.command(name='setplay',
                      description="change the game tag off the bot [ADMIN ONLY]",
                      brief="change the game tag")
    @commands.has_permissions(administrator=True)
    async def setplay(self, ctx,*, play):
        await self.bot.change_presence(game=discord.Game(name=play))

    @commands.command(name='info',
                      description="get info on a specific user",
                      brief="info of a user")
    async def info(self, ctx):
        for user in ctx.message.mentions:
            member = ctx.message.server.get_member(user.id)
            embed_colour = self.bot.embed_color
            if member.colour != member.colour.default():
                embed_colour = member.colour.value
            embed = discord.Embed(title=str(user), url=user.avatar_url, description=user.display_name, color=embed_colour)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name='Is bot', value=user.bot, inline=True)
            embed.add_field(name='Voice channel', value=user.voice_channel, inline=True)
            role_list = "None"
            if len(member.roles) > 1:
                role_array = []
                for role in member.roles:
                    role_array.append(role.name)
                role_array.pop(0)
                role_array.reverse()
                role_list = ', '.join(role_array)
            embed.add_field(name='Roles', value=role_list, inline=False)
            embed.add_field(name='Playing', value=member.game, inline=False)
            embed.add_field(name='Joined discord at', value=user.created_at, inline=True)
            embed.add_field(name='Joined server at', value=member.joined_at, inline=True)
            await ctx.send(embed=embed)

    @commands.command(name='serverinfo',
                      description="get info on the server",
                      brief="server info")
    async def serverinfo(self, ctx):
        guild = ctx.message.guild
        total = len(ctx.message.guild.members)
        bot  = 0
        online = 0
        gaming = 0
        for member in guild.members:
            if member.bot:
                bot += 1
            if member.status != discord.Status.offline:
                online += 1
            if member.activity:
                gaming += 1
        embed = discord.Embed(
            title="serverInfo",
            description=guild.name,
            color=self.bot.embed_color
        )
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='Owner', value=guild.owner, inline=False)
        embed.add_field(name='Region', value=guild.region, inline=False)
        text_channel = 0
        voice_channel = 0
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                text_channel += 1
            elif channel.type == discord.ChannelType.voice:
                voice_channel += 1
        embed.add_field(name='Text Channels', value=text_channel, inline=False)
        embed.add_field(name='Voice Channels', value=voice_channel, inline=False)
        embed.add_field(name='Members', value=total, inline=False)
        embed.add_field(name='Humans', value=total-bot, inline=False)
        embed.add_field(name='Bots', value=bot, inline=False)
        embed.add_field(name='Gaming', value=gaming, inline=False)
        embed.add_field(name='Online', value=online, inline=False)
        embed.add_field(name='Roles', value=len(guild.roles), inline=False)
        await ctx.send(embed=embed)
        
    @commands.command(name='say',
                      description="bot sends query and deletes trigger message",
                      brief="bot sends query")
    async def say(self, ctx, *,word):
        await ctx.message.delete()
        await ctx.send(word)

def setup(bot):
    bot.add_cog(Manage(bot))
