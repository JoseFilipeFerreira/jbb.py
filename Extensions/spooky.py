import discord
from discord.ext import commands

class Spooky():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def submode(self, ctx, ch):
        channel = ctx.message.server.get_channel(ch[2:len(ch) - 1])
        role = ctx.message.server.default_role
        perms = discord.PermissionOverwrite()
        perms.send_messages = toggle_overwrite(channel)
        await self.bot.edit_channel_permissions(channel, role, perms)
        mode = ""
        if perms.send_messages == False:
            mode = "enabled"
        else:
            mode = "disabled"

        await self.bot.say("Sub only mode " + mode)

def toggle_overwrite(channel):
    perms = channel.overwrites_for(channel.server.default_role)
    if perms.send_messages == False:
        return None
    else:
        return False

def setup(bot):
    bot.add_cog(Spooky(bot))
