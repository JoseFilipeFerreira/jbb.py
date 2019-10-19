import discord
from discord.ext import commands
import json
from aux.stats import Stats

class Biography(commands.Cog):
    """Server member's biography"""
    
    def __init__(self, bot):
        self.bot = bot
        self.biographies = json.load(open(bot.BIOGRAPHY_PATH, 'r', encoding="utf8"))["bios"]
        self.order       = json.load(open(bot.BIOGRAPHY_PATH, 'r', encoding="utf8"))["order"]

    @commands.command(
        name='bio',
        description="send a funy description of a given user",
        brief="get one's biography")
    async def bio(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.message.author
        embed_colour = self.bot.embed_color 
        if member.colour != member.colour.default():
            embed_colour = member.colour.value
            
        embed = discord.Embed(
            title = 'Biography of {}'.format(member.display_name),
            color=embed_colour)
        embed.set_thumbnail(
            url="https://img9.androidappsapk.co/300/e/a/2/com.sdvios.png")

        if member.id in self.biographies:
            bio = self.biographies[member.id]
            for key in self.order:
                if key in bio:
                    embed.add_field(
                        name=key,
                        value="\n".join(bio[key]))

        k, d = self.bot.stats.get_kdr(member.id)
        embed.add_field(
            name="🔫KDR",
            value="{0}/{1}".format(k, d))
            
        embed.set_footer(text = "Biography")
        await ctx.send(embed=embed)
        await ctx.send(embed=self.bot.stats.get_embed_inventory(member.id, member.display_name, embed_colour))

    @commands.command(
        name='bioKey',
        brief="alter bio keys")
    @commands.is_owner()
    async def bioKey(self, ctx, modifier,* text):
        """**MODIFIERS:**
        **list:**   send all available bio keys
        **add:**    add a bio key
        **swap:**   swap two bioKeys' position
        **delete:** delete a given position"""

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
        brief="add one's biography")
    @commands.is_owner()
    async def editBio(self, ctx, member : discord.Member,  action, bioKey, *, text):
        """add a funy description of a given user
        **ACTIONS:**
        **delete:** delete a given position
        **add:** add a description"""
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
