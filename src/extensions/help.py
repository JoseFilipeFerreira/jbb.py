import discord
from discord.ext import commands
import json
import subprocess
import time

class Help(commands.Cog):
    """Help command"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help",
                      description="Sends help for a specific command or cog",
                      brief="shows this message")
    async def help(self, ctx, *, command_or_cog=None):
        if not command_or_cog:
            await help_all(self, ctx)
        elif command_or_cog in self.bot.cogs:
            await help_cog(self, ctx, command_or_cog)
        elif command_or_cog in map(lambda e: str(e), list(self.bot.walk_commands())):
            await help_command(self, ctx, command_or_cog)
        else:
            await ctx.send("Command or cog not found")

    @commands.command(name='helpPlay',
                      description="list all available musics",
                      brief="all available musics")
    async def helpPlay(self, ctx):
        await MenuGenerateEmbed(self, ctx, self.bot.musicMap,"Music", "available music in jukebox:")

    @commands.command(name='helpImage',
                      description="list all available Images",
                      brief="all available Images")
    async def helpImage(self, ctx):
        await MenuGenerateEmbed(self, ctx, self.bot.imagesMap,"Image", "available memes and photos:")

    @commands.command(name='helpGif',
                      description="list all available gifs",
                      brief="all available gifs")
    async def helpGif(self, ctx):
        await MenuGenerateEmbed(self, ctx, self.bot.gifsMap,"Gif", "available Gif/Jif:")

def setup(bot):
    bot.add_cog(Help(bot))

async def help_all(self, ctx):
#send help
    cogs = self.bot.cogs

    string_cogs = ""
    for cog in cogs.keys():
       string_cogs += "**{0}**\n".format(cog)

    embed = discord.Embed(
        title="List of all available cogs:",
        description=string_cogs,
        color=self.bot.embed_color)

    embed.set_footer(
        text=f"{self.bot.command_prefix}help [cog] para saberes mais sobre alguma cog")

    await ctx.send(embed=embed)

async def help_cog(self, ctx, command_or_cog):
#send help for a cog

    string_commands = ""
    cog = None
    list_commands = []
    for command in self.bot.commands:
        if command.cog_name == command_or_cog and command not in list_commands:
            cog = command.cog
            string_commands = string_commands + f"**{command.name}** -> {command.brief}\n"
            list_commands.append(command)

    embed = discord.Embed(
        title=command_or_cog,
        description=cog.description,
        color=self.bot.embed_color)

    embed.add_field(
        name="Commands in Cog:",
        value=string_commands,
        inline=False)

    embed.set_footer(
        text=f"{self.bot.command_prefix}help [comando] para saberes mais sobre algum comando")

    await ctx.send(embed=embed)

async def help_command(self, ctx, command_or_cog):
#send help for a command
    command = None

    for c in self.bot.walk_commands():
        if command_or_cog.lower() == str(c).lower():
            command = c

    embed = discord.Embed(
        title="Comando",
        description=command.qualified_name,
        color=self.bot.embed_color)

    embed.add_field(
        name="DESCRIPTION",
        value=command.help if command.help != None else command.description,
        inline=False)

    synopse = self.bot.command_prefix + command.name
    for param in command.clean_params.keys():
        synopse = synopse + " [" + param + "]"

    embed.add_field(
        name="SYNOPSE",
        value="`" + synopse + "`",
        inline=False)

    if len(command.aliases) > 0:
        embed.add_field(
            name="ALIASES",
            value="; ".join(command.aliases),
            inline=False)

    await ctx.send(embed=embed)

async def MenuGenerateEmbed(self, ctx, thingMap, title, section):
#generate a embed for a menu
    embed=discord.Embed(
        title=title,
        description=" ",
        color=self.bot.embed_color
    )
    musicArray = []
    for music in thingMap:
        musicArray.append(music)
    musicArray.sort()
    embed.add_field(name=section, value='\n'.join(musicArray), inline=True)
    await ctx.message.author.send(embed=embed)
    await ctx.message.delete()
