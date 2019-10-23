import discord
import asyncio

async def userInputTrueFalse(bot, author, msg):
    await msg.add_reaction('\U0000274C')
    await msg.add_reaction('\U00002705')

    def check(reaction, user):
        return user == author and str(reaction.emoji) in ['\U00002705', '\U0000274C']  
    
    try:
        reaction, _ = await bot.wait_for(
                'reaction_add',
                timeout=10.0,
                check=check)
    except asyncio.TimeoutError:
        await msg.clear_reactions()
        return False

    await msg.clear_reactions()
    if reaction.emoji ==  '\U0000274C':
        return False

    return True
