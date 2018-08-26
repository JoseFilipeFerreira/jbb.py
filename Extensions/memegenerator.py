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
    async def meme(self, ctx, image, *text):
    #generate meme
        image = image.lower()
        #"parse" information to draw
        if (len(text) == 0):
            top = " "
            bottom = " "
        elif(len(text) == 1):
            top = text[0]
            bottom = " "
        else:
            top = text[0]
            bottom = text[1]
        
        if image in self.bot.imagesMap:
            img = Image.open(self.bot.IMAGES_PATH + self.bot.imagesMap[image])
            draw = ImageDraw.Draw(img)
        
            fontTop, w1, h1 = getFittingFont(img, "impact.ttf", top)
            fontBottom, w2, h2 = getFittingFont(img, "impact.ttf", bottom)

            drawTextWithOutline(draw, fontTop, top, img.width/2 - w1/2, 10)
            drawTextWithOutline(draw, fontBottom, bottom, img.width/2 - w2/2, img.height-52)

            img.save(self.bot.MEMEGENERATOR_PATH + "tmp.png")
    
            await self.bot.delete_message(ctx.message)
            await self.bot.send_file(
                ctx.message.channel,
                self.bot.MEMEGENERATOR_PATH + "tmp.png",
                content='by {}'.format(ctx.message.author.mention))
        else:
            await self.bot.say("Invalid image name!")


def drawTextWithOutline(draw, font, text, x, y):
    draw.text((x-2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y+2), text,(0,0,0),font=font)
    draw.text((x-2, y+2), text,(0,0,0),font=font)
    draw.text((x, y), text, (255,255,255), font=font)
    return


def getFittingFont(img, fontName, text):
    #get font that fits in image
    textSize = 42
    font = ImageFont.truetype(fontName, textSize)
    w, h = font.getsize(text)
    if (w > img.width and textSize > 1):
        while(w > img.width and textSize > 1):
            textSize = textSize - 1
            font = ImageFont.truetype(fontName, textSize)
            w, h = font.getsize(text)
    return font, w, h

def setup(bot):
    bot.add_cog(Memegenerator(bot))
