import json
from discord.ext import commands
from github import Github

class Dotfiles(commands.Cog):
    """Server member's dotfiles"""

    def __init__(self, bot):
        self.bot = bot
        with open(bot.DOTFILES_PATH, 'r') as file:
            self.repos = json.load(file)
        self.github = Github(bot.config['credentials']['github'])

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
            repo = self.github.get_repo(self.repos[owner].replace('https://github.com/', ''))
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

    @commands.command(
        name='resumos',
        description="manage resumos\n\nresumos\nresumos [FILE/FOLDER]\nresumos [FOLDER] [FILE]",
        brief="manage resumos")
    async def resumos(self, ctx,* args):
        site = 'https://git.mendess.xyz/ResumosMIEI/'
        repo = 'mendess/ResumosMIEI'

        if len(args) == 0:
            await ctx.send(site)
            return

        repo = self.github.get_repo(repo)
        contents = repo.get_contents("")

        searched_repo = None

        if len(args) == 1:
            while contents:
                file_content = contents.pop(0)
                if args[0].lower() in file_content.path.lower():
                    searched_repo = file_content
                    break
                elif file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))

        elif len(args) == 2:
            folder = args[0].lower()
            file = args[1].lower()

            folder_contents = None
            while contents:
                content = contents.pop(0)
                if content.type == "dir" and folder in content.path.lower():
                    folder_contents = repo.get_contents(content.path)
                    break

            if not folder_contents:
                await ctx.send('Folder does not exist')
                return

            while folder_contents:
                file_content = folder_contents.pop(0)
                if file_content.type == "dir":
                    folder_contents.extend(repo.get_contents(file_content.path))
                elif file in file_content.name.lower():
                    searched_repo = file_content
                    break
        else:
            await ctx.send('Invalid number of arguments')

        if not searched_repo:
            await ctx.send("No file found")
            return

        web = searched_repo.html_url
        web = web.replace(
            'https://github.com/mendess/ResumosMIEI/blob/master/',
            site)
        web = web.replace(
            'https://github.com/mendess/ResumosMIEI/tree/master/',
            site)
        if '.' in web.split('/')[-1]:
            web = web.replace(web.split('.')[-1], 'html')
        await ctx.send(web)

def setup(bot):
    bot.add_cog(Dotfiles(bot))
