import discord
import json
import subprocess
import random
import string
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class Memegenerator():
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def meme(self, ctx, image, top, bottom):
        if (not top): top = " "
        if (not bottom): bottom = " "
        img = Image.open("Images/{}.png".format(image))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("impact.ttf", 42)
        w1, h1 = draw.textsize(top, font) # measure the size the text will take
        w2, h2 = draw.textsize(bottom, font)
        drawTextWithOutline(draw, font, top, img.width/2 - w1/2, 10)
        drawTextWithOutline(draw, font, bottom, img.width/2 - w2/2, img.height-52)

        name = getRandomName(20)
        img.save("Memegenerator/{}.png".format(name))
    
        await self.bot.delete_message(ctx.message)
        await self.bot.send_file(ctx.message.channel, "Memegenerator/{}.png".format(name))
        await self.bot.say('by {}'.format(ctx.message.author.mention))

def setup(bot):
    bot.add_cog(Memegenerator(bot))


def drawTextWithOutline(draw, font, text, x, y):
    draw.text((x-2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y+2), text,(0,0,0),font=font)
    draw.text((x-2, y+2), text,(0,0,0),font=font)
    draw.text((x, y), text, (255,255,255), font=font)
    return

def getRandomName(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))