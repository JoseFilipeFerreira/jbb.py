import discord
from discord.ext import commands
import sys
import traceback

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command."""

        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(f"{ctx.command} can't be used in Private Messages.")
        
        elif isinstance(error, discord.ext.commands.errors.NSFWChannelRequired):
                return await ctx.send(f'Command must be done in {get_NSFW(ctx)}')
            
        elif isinstance(error, discord.ext.commands.errors.NotOwner):
                return await ctx.send('Owner only command')

        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
                return await ctx.send("You don't have permissions for this command")

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot)) 

def get_NSFW(ctx):
    listChannels = []
    for channel in ctx.guild.channels:
        if channel.type == discord.ChannelType.text:
            if channel.is_nsfw():
                #if channel.overwrites_for(ctx.guild.default_role):
                if channel.name != "test-in-prod":
                    listChannels.append(channel.mention)
    return ' '.join(listChannels)

