import discord
from discord.ext import commands


class Ascii():
    #module for ascii art
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='asciihum',
                      description="gives a thinking emoji in ascii code",
                      brief="thinking emoji",
                      aliases=['hum', 'thinking'],
                      pass_context=True)
    async def asciihum(self):
        a = ("▒▒▒▒▒▒▒▒▄▄▄▄▄▄▄▄▒▒▒▒▒▒▒▒\n"
             "▒▒▒▒▒▄█▀▀░░░░░░▀▀█▄▒▒▒▒▒\n"
             "▒▒▒▄█▀▄██▄░░░░░░░░▀█▄▒▒▒\n"
             "▒▒█▀░▀░░▄▀░░░░▄▀▀▀▀░▀█▒▒\n"
             "▒█▀░░░░███░░░░▄█▄░░░░▀█▒\n"
             "▒█░░░░░░▀░░░░░▀█▀░░░░░█▒\n"
             "▒█░░░░░░░░░░░░░░░░░░░░█▒\n"
             "▒█░░██▄░░▀▀▀▀▄▄░░░░░░░█▒\n"
             "▒▀█░█░█░░░▄▄▄▄▄░░░░░░█▀▒\n"
             "▒▒▀█▀░▀▀▀▀░▄▄▄▀░░░░▄█▀▒▒\n"
             "▒▒▒█░░░░░░▀█░░░░░▄█▀▒▒▒▒\n"
             "▒▒▒█▄░░░░░▀█▄▄▄█▀▀▒▒▒▒▒▒\n"
             "▒▒▒▒▀▀▀▀▀▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒\n")
        await self.bot.say(a)

def setup(bot):
    bot.add_cog(Ascii(bot))
