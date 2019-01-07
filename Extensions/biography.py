import discord
import json
from discord.ext import commands
from random import choice

class Biography():
    
    def __init__(self, bot):
        self.bot = bot
        with open(bot.BIOGRAPHY_PATH, 'r', encoding="utf8") as file:
            self.biography = json.load(file)

    @commands.command(
        name='bio',
        description="send a funy description of a given user",
        brief="get one's biography",
        pass_context=True)
    async def bio(self, ctx):
        await self.bot.say("kuku")

def setup(bot):
    bot.add_cog(Biography(bot))

def updateBio(self, bio):
#update a JSON file
    with open(self.bot.BIOGRAPHY_PATH, 'w', encoding='utf8') as file:
        json.dump(bio, file, indent=4)