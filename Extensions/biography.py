import discord
import json
from discord.ext import commands
from random import randint
from aux.inventory import get_embed_inventory

class Biography(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.biographies = json.load(open(bot.BIOGRAPHY_PATH, 'r', encoding="utf8"))["bios"]
        self.order       = json.load(open(bot.BIOGRAPHY_PATH, 'r', encoding="utf8"))["order"]

    @commands.command(
        name='bio',
        description="send a funy description of a given user",
        brief="get one's biography")
    async def bio(self, ctx):
        for user in ctx.message.mentions:
            member = ctx.message.server.get_member(user.id)
            name = member.name
            if member.nick != None:
                name = member.nick
  
            embed_colour = self.bot.embed_color 
            if member.colour != member.colour.default():
                embed_colour = member.colour.value
            
            embed = discord.Embed(
                title = 'Biography of {}'.format(name),
                color=embed_colour
            )
            embed.set_thumbnail(
                url="https://img9.androidappsapk.co/300/e/a/2/com.sdvios.png"
            )

            if user.id in self.biographies:
                bio = self.biographies[user.id]
                for key in self.order:
                    if key in bio:
                        embed.add_field(
                            name=key,
                            value="\n".join(bio[key])
                        )

            embed.add_field(
                name="🔫KDR",
                value="{0}/{1}".format(self.bot.stats[user.id]["kills"], self.bot.stats[user.id]["death"]))
            
            embed.set_footer(text = "Biography")
            await self.bot.say(embed=embed)
            await self.bot.say(embed=get_embed_inventory(self.bot, user.id, name, embed_colour))

    @commands.command(
        name='bioKey',
        description="**MODIFIERS:**\n**list:**   send all available bio keys\n**add:**    add a bio key\n**swap:**   swap two bioKeys' position\n**delete:** delete a given position",
        brief="alter bio keys")
    @commands.is_owner()
    async def bioKey(self, ctx, modifier,* text):
        #list all bioKeys
        if modifier == "list":
            await self.bot.say(textKeyOrder(self.order))
        
        #add a bioKey
        elif modifier == "add":
            if len(text) != 1:
                await self.bot.say("Invalid parameters")
                return
            bioKey = text[0]
            bioKeys = self.order
            bioKeys.append(bioKey)
            self.order = bioKeys
            updateBio(self)
            await self.bot.say("New Key added:\n" + bioKey)

        #reorder bioKey
        elif modifier == "swap":
            if len(text) != 2:
                await self.bot.say("Invalid parameters")
                return
            pos1 = int(text[0])
            pos2 = int(text[1])
            self.order[pos1], self.order[pos2] = self.order[pos2], self.order[pos1]
            await self.bot.say(textKeyOrder(self.order))
            updateBio(self)

        #delete bioKey
        elif modifier == "delete":
            if len(text) != 1:
                await self.bot.say("Invalid parameters")
                return
            pos = int(text[0])
            self.order.pop(pos)
            await self.bot.say(textKeyOrder(self.order))
            updateBio(self)
        else:
            await self.bot.say("Invalid modifier")

    @commands.command(
        name='editBio',
        description="add a funy description of a given user\n**ACTIONS:**\n**delete:** delete a given position\n**add:** add a description",
        brief="add one's biography")
    @commands.is_owner()
    async def editBio(self, ctx, member,  action, bioKey, *, text):
        #check member
        server = ctx.message.server
        memberId = list(filter(lambda x: x.isdigit(), member))
        memberId = "".join(memberId)
        if not len(memberId) in [17, 18]:
            await self.bot.say("Invalid member")
            return
        member = server.get_member(memberId)
        
        #check bioKey
        if bioKey not in self.order:
            await self.bot.say("Invalid bioKey")
            return

        if action == "delete":
            ptext = text.split(" ")
            if len(ptext) != 1:
                await self.bot.say("Invalid parameters")
                return
            self.biographies[memberId][bioKey].pop(int(ptext[0]))
            #delete bioKey if empty
            if len(self.biographies[memberId][bioKey]) == 0:
               self.biographies[memberId].pop(bioKey, None)
            #delete bio if empty
            if len(self.biographies[memberId].keys()) == 0:
                self.biographies.pop(memberId, None)
            await self.bot.say("bioKey removed")
               
        elif action == "add":
            if memberId not in self.biographies:
                self.biographies[memberId] = {}
            if bioKey not in self.biographies[memberId]:
                self.biographies[memberId][bioKey] = []
            self.biographies[memberId][bioKey].append(text)
            await self.bot.say("bioKey added")

        updateBio(self)

def setup(bot):
    bot.add_cog(Biography(bot))
    
def textKeyOrder(order):
#generates the text of the bio Keys
    keyText = "**Available Keys:**"
    id = 0
    for bioKey in order:
        keyText = keyText + "\n" + str(id) + ". " + bioKey
        id += 1
    return keyText

def updateBio(self):
#update a JSON file
    with open(self.bot.BIOGRAPHY_PATH, 'w', encoding='utf8') as file:
        json.dump({"bios": self.biographies, "order": self.order}, file, indent=4)
