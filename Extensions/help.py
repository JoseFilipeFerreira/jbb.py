import discord
import json
import subprocess
import time
from discord.ext import commands

class Help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help",
                      description="Sends help for a specific command or cog",
                      brief="shows this message")
    async def help(self, ctx, * command_or_cog):
        cogs = self.bot.cogs
        commands = self.bot.commands

        if len(command_or_cog) == 0:
            await help_all(self)
        
        else:
            command_or_cog = command_or_cog[0]
            if command_or_cog in cogs.keys():
                await help_cog(self, command_or_cog)
            elif command_or_cog in commands.keys():
                await help_command(self, command_or_cog)
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

async def help_all(self):
#send help
    cogs = self.bot.cogs

    string_cogs = ""
    for cog in cogs.keys():
        string_cogs = string_cogs + "**{0}**\n".format(cog)

    embed = discord.Embed(
        title="List of all available cogs:",
        description=string_cogs,
        color=self.bot.embed_color)
    
    embed.set_footer(
        text="{}help [cog] para saberes mais sobre alguma cog".format(self.bot.command_prefix))
    
    await ctx.send(embed=embed)

async def help_cog(self, command_or_cog):
#send help for a cog
    commands = self.bot.commands
            
    embed = discord.Embed(
        title=command_or_cog,
        description="help command shitshow",
        color=self.bot.embed_color)

    string_commands = ""
    list_commands = []
    for command in commands.keys():
        command = commands[command]
        if command.cog_name == command_or_cog and command not in list_commands:
            string_commands = string_commands + "**{0}** -> {1}\n".format(command.name, command.brief)
            list_commands.append(command)

    embed.add_field(
        name="Commands in Cog:",
        value=string_commands,
        inline=False)
            
    embed.set_footer(
        text="{}help [comando] para saberes mais sobre algum comando".format(self.bot.command_prefix))
            
    await ctx.send(embed=embed)

async def help_command(self, command_or_cog):
#send help for a command
    commands = self.bot.commands
    command = commands[command_or_cog]

    embed = discord.Embed(
        title="Comando",
        description=command.qualified_name,
        color=self.bot.embed_color)
            
    embed.add_field(
        name="DESCRIPTION",
        value=command.description,
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
            value=command.aliases,
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
    await self.bot.send_message(ctx.message.author, embed=embed)
    await self.bot.delete_message(ctx.message)
