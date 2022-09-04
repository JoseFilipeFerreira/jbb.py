import json
import discord
from discord.ext import commands

class Biography(commands.Cog):
    """Server member's biography"""

    def __init__(self, bot):
        self.bot = bot
        with open(bot.BIOGRAPHY_PATH, 'r', encoding="utf8") as file:
            self.biographies = json.load(file)["bios"]
        with open(bot.BIOGRAPHY_PATH, 'r', encoding="utf8") as file:
            self.order = json.load(file)["order"]

    @commands.command(
        name='bio',
        description="send a funny description of a given user",
        brief="get one's biography")
    async def bio(self, ctx, member : discord.Member = None):
        if member is None:
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
            await self.bot.say(text_key_order(self.order))

        #add a bioKey
        elif modifier == "add":
            if len(text) != 1:
                await self.bot.say("Invalid parameters")
                return
            bio_key = text[0]
            bio_keys = self.order
            bio_keys.append(bio_key)
            self.order = bio_keys
            update_bio(self)
            await self.bot.say("New Key added:\n" + bio_key)

        #reorder bioKey
        elif modifier == "swap":
            if len(text) != 2:
                await self.bot.say("Invalid parameters")
                return
            pos1 = int(text[0])
            pos2 = int(text[1])
            self.order[pos1], self.order[pos2] = self.order[pos2], self.order[pos1]
            await self.bot.say(text_key_order(self.order))
            update_bio(self)

        #delete bioKey
        elif modifier == "delete":
            if len(text) != 1:
                await self.bot.say("Invalid parameters")
                return
            pos = int(text[0])
            self.order.pop(pos)
            await self.bot.say(text_key_order(self.order))
            update_bio(self)
        else:
            await self.bot.say("Invalid modifier")

    @commands.command(
        name='editBio',
        brief="add one's biography")
    @commands.is_owner()
    async def editBio(self, ctx, member : discord.Member,  action, bio_key, *, text):
        """add a funy description of a given user
        **ACTIONS:**
        **delete:** delete a given position
        **add:** add a description"""
        #check bioKey
        if bio_key not in self.order:
            await self.bot.say("Invalid bioKey")
            return

        if action == "delete":
            ptext = text.split(" ")
            if len(ptext) != 1:
                await self.bot.say("Invalid parameters")
                return
            self.biographies[member.id][bio_key].pop(int(ptext[0]))
            #delete bioKey if empty
            if len(self.biographies[member.id][bio_key]) == 0:
               self.biographies[member.id].pop(bio_key, None)
            #delete bio if empty
            if len(self.biographies[member.id].keys()) == 0:
                self.biographies.pop(member.id, None)
            await self.bot.say("bioKey removed")

        elif action == "add":
            if member.id not in self.biographies:
                self.biographies[member.id] = {}
            if bio_key not in self.biographies[member.id]:
                self.biographies[member.id][bio_key] = []
            self.biographies[member.id][bio_key].append(text)
            await self.bot.say("bioKey added")

        update_bio(self)

    @commands.command(
        name='avatar',
        brief='Get own or mentioned users avatar')
    async def avatar(self, ctx, args: discord.User=None):
        num_mentioned_users = len(ctx.message.mentions)
        # Mentioning multiple users in this command will
        # not send the avatar of any user
        if num_mentioned_users > 1:
            await ctx.send("Mentioned more than 1 user")
        else:
            embed = discord.Embed(color=self.bot.embed_color)
            # 'args' will be only the first mention of the message
            # if no mention is provided then send the author's avatar
            if args is None :
                embed.set_image(url=ctx.message.author.avatar_url)
            else:
                embed.set_image(url=args.avatar_url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Biography(bot))

def text_key_order(order):
#generates the text of the bio Keys
    keyText = "**Available Keys:**"
    id = 0
    for bio_key in order:
        keyText = keyText + "\n" + str(id) + ". " + bio_key
        id += 1
    return keyText

def update_bio(self):
#update a JSON file
    with open(self.bot.BIOGRAPHY_PATH, 'w', encoding='utf8') as file:
        json.dump({"bios": self.biographies, "order": self.order}, file, indent=4)
