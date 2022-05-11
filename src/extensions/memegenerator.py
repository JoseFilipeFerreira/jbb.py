import discord
from discord.ext import commands
import subprocess
from PIL import Image, ImageFont, ImageDraw

class Memegenerator(commands.Cog):
    """Generate dank memes"""    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='meme',
                      description="creates a meme with given arguments",
                      brief="create a meme")
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
        
            fontTop, w1, _ = getFittingFont(img, self.bot.IMPACT_PATH, top)
            fontBottom, w2, h2 = getFittingFont(img, self.bot.IMPACT_PATH, bottom)

            drawTextWithOutline(draw, fontTop, top, img.width/2 - w1/2, 0)
            drawTextWithOutline(draw, fontBottom, bottom, img.width/2 - w2/2, img.height-h2-7)

            img.save(self.bot.TMP_PATH + "memegenerator.png")
    
            await ctx.message.delete()
            await ctx.send(
                'by {}'.format(ctx.message.author.mention),
                file=discord.File(
                    self.bot.TMP_PATH + "memegenerator.png"))
        else:
            await ctx.send("Invalid image name!")


def drawTextWithOutline(draw, font, text, x, y):
    draw.text((x-2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y+2), text,(0,0,0),font=font)
    draw.text((x-2, y+2), text,(0,0,0),font=font)
    draw.text((x, y), text, (255,255,255), font=font)
    return


def getFittingFont(img, fontName, text):
    #get font that fits in image
    textSize = 50
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
