import discord
from discord.ext import commands
import json
import os
import subprocess
import time

class Manage(commands.Cog):
    """Manage the server"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='update',
                      description="update the code from github and reboot [OWNER ONLY]",
                      brief="update the bot")
    @commands.is_owner()
    async def update(self, ctx):
        await self.bot.change_presence(activity=discord.Game(name='rebooting'))
        await self.bot.logout()

    @commands.command(name='eval',
                      description="run random python code [OWNER ONLY]",
                      brief="built in eval")
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        evaluated = ""
        try:
            evaluated = eval(code)
        except Exception as e:
            evaluated = str(e)
        await ctx.send("**{0}**\n```\n{1}\n```".format(code, evaluated))

    @commands.command(name='setplay',
                      description="change the game tag off the bot [ADMIN ONLY]",
                      brief="change the game tag")
    @commands.has_permissions(administrator=True)
    async def setplay(self, ctx,*, play):
        await self.bot.change_presence(game=discord.Game(name=play))

    @commands.command(name='live',
                      description="get link for multi-webcam chat on server",
                      brief="go live")
    @commands.has_permissions(administrator=True)
    async def live(self, ctx):
        vcState = ctx.message.author.voice
        if vcState == None:
            ctx.send("No voice state")
            return
        channel = vcState.channel
        if channel == None:
            ctx.send("Not in a voice channel")
            return
        await ctx.send("WebCam Show Live!😉 \n<https://www.discordapp.com/channels/{0}/{1}>".format(ctx.guild.id, channel.id))

    @commands.command(name='info',
                      description="get info on a specific user",
                      brief="info of a user")
    async def info(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.message.author
        embed_colour = self.bot.embed_color
        if member.colour != member.colour.default():
            embed_colour = member.colour.value
        embed = discord.Embed(
                title=str(member),
                url=str(member.avatar_url_as(format="png")),
                description=member.display_name,
                color=embed_colour)
        embed.set_thumbnail(
                url=str(member.avatar_url_as(format="png")))
        embed.add_field(
                name='Is bot',
                value=member.bot,
                inline=True)
        embed.add_field(
                name='Voice channel',
                value="[REDACTED]" if member.voice else "None",
                inline=True)
        role_list = "None"
        if len(member.roles) > 1:
            role_array = []
            for role in member.roles:
                role_array.append(role.name)
            role_array.pop(0)
            role_array.reverse()
            role_list = ', '.join(role_array)
        embed.add_field(
                name='Roles',
                value=role_list,
                inline=False)
        embed.add_field(
                name='Playing',
                value=member.activity,
                inline=False)
        embed.add_field(
                name='Joined discord at',
                value=member.created_at,
                inline=True)
        embed.add_field(
                name='Joined server at',
                value=member.joined_at,
                inline=True)
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
            color=self.bot.embed_color)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(
                name='Region',
                value=guild.region,
                inline=False)
        text_channel = 0
        voice_channel = 0
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                text_channel += 1
            elif channel.type == discord.ChannelType.voice:
                voice_channel += 1
        embed.add_field(
                name='Text Channels',
                value=text_channel,
                inline=True)
        embed.add_field(
                name='Voice Channels',
                value=voice_channel,
                inline=True)
        embed.add_field(
                name='Roles',
                value=len(guild.roles),
                inline=False)
        embed.add_field(
                name='Members',
                value=total,
                inline=True)
        embed.add_field(
                name='Humans',
                value=total-bot,
                inline=True)
        embed.add_field(
                name='Online',
                value=online,
                inline=False)
        embed.add_field(
                name='Gaming',
                value=gaming,
                inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='say',
                      description="bot sends query and deletes trigger message",
                      brief="bot sends query")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *,word):
        await ctx.message.delete()
        await ctx.send(word)

    @commands.command(name='slowmode',
                      description="",
                      brief="")
    @commands.has_permissions(administrator=True)
    async def slowmode(self, ctx, args, user_id = None):
        if args:
            if user_id is not None:
                user = ctx.guild.get_member(int(user_id))
                if user is not None:
                    if args.lower() == "add":
                        self.bot.slow_users['users'][user_id] = time.time()
                        await ctx.send("{} was added to the slowmode list".format(user.display_name))
                    elif args.lower() == "rm":
                        self.bot.slow_users['users'].pop(user_id, None)
                        await ctx.send("{} was removed to the slowmode list".format(user.display_name))
                elif args.lower() == "set":
                    self.bot.slow_users['time'] = int(user_id)
                    await ctx.send("Cooldown is now set to {} minutes".format(user_id))
            elif args.lower() == "info":
                cooldown_users = ",".join(list(map(lambda x: ctx.guild.get_member(int(x)).display_name, self.bot.slow_users['users'].keys())))
                await ctx.send("Cooldown time: {} minutes\nCooldown users: {}".format(self.bot.slow_users['time'], cooldown_users))

            with open(self.bot.SLOWMODE_PATH, 'w', encoding='utf8') as file:
                json.dump(self.bot.slow_users, file, indent=4)

def setup(bot):
    bot.add_cog(Manage(bot))
