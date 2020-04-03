import discord
from discord.ext import commands
from github import Github
import json

class Dotfiles(commands.Cog):
    """Server member's dotfiles"""

    def __init__(self, bot):
        self.bot = bot
        self.repos = json.load(open(bot.DOTFILES_PATH, 'r'))
        self.g = Github(open('auth_github').readline().rstrip())

    @commands.command(
        name='dotfile',
        description="manage member's dotfiles\n\ndotfile add [LINK]\ndotfile [FILE]\ndotfile",
        brief="manage dotfiles")
    async def dotfile(self, ctx,* args):
        owner = str(ctx.message.author.id)

        if len(args) == 2:
            if args[0] == "add":
                if 'https://github.com/' not in args[1]:
                    await ctx.send("Invalid args")
                else:
                    self.repos[owner] = args[1]
                    with open(self.bot.DOTFILES_PATH, 'w') as file:
                        json.dump(self.repos, file, indent=4)
                    await ctx.send("Repo added to user")
            else:
                await ctx.send("Invalid number of arguments")

        elif owner not in self.repos:
            await ctx.send("You don't have an associated repo")

        elif len(args) == 0:
            await ctx.send(self.repos[owner])

        else:
            repo = self.g.get_repo(self.repos[owner].replace('https://github.com/', ''))
            contents = repo.get_contents("")
            searched_repo = None

            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                elif args[0].lower() in file_content.name.lower():
                    searched_repo = file_content
                    break

            if not searched_repo:
                await ctx.send("No file found")
            else:
                await ctx.send(searched_repo.html_url)

def setup(bot):
    bot.add_cog(Dotfiles(bot))

