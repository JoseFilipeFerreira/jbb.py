import discord
from discord.ext import commands
from baseconvert import base
from random import choice

class ReadMatrix(commands.Converter):
    async def convert(self, ctx, matrix):
        matrix = ''.join(c for c in matrix if c.isdigit() or c.isspace() or c in [';', ','])
        matrix = matrix.replace(',',' ').split(';')
        matrix = map(lambda x : x.split(), matrix)
        matrix = map(lambda x : list(map(float, x)), matrix)
        return list(matrix)

class Programming(commands.Cog):
    """Programming help"""    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='helpHaskell',
                      description="give overlycomplicated function that returns the double of a given number in haskell",
                      brief="small program in haskell")
    async def helpHaskell(self, ctx):
        doublFct = ['double = foldr (+) 0 . take 2 . repeat', 
            'double = foldr (+) 0 . take 2 . cycle . return',
            'double = head . fmap ap . zip [(2*)] . return',
            'double = succ . (!!2) . enumFromThen 1',
            'double = uncurry (+) . dup',
            'double x = x + x']
        await ctx.send('```Haskell\ndouble :: Double -> Double\n' + choice(doublFct) + '```')

    @commands.command(name='quicksort',
                      description="help understand quicksort",
                      brief="quicksort is hard guys",
                      aliases=["qsort"])
    async def quicksort(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=ywWBy6J5gz8')

    @commands.command(name='convert',
                      description="convert between numeric bases",
                      brief="convert between bases",
                      aliases=["conv"])
    async def convert(self, ctx, number, basefrom : int, baseto :int ):
        result = base(number, basefrom, baseto, string=True)
        await ctx.send('{0} na base {1} para base {2} dá:\n{3}'
                .format(number, basefrom, baseto, result))

    @commands.command(name='lmgtfy',
                      description="give link for let me google that for you",
                      brief="let me google that for you")
    async def lmgtfy(self, ctx, *query):
        await ctx.send(f"http://lmgtfy.com/?q={'+'.join(word for word in query)}")

    @commands.command(name='gauss',
                      brief="método de eliminação de gauss",
                      aliases=['egpp'])
    async def gauss(self, ctx, *, matrix : ReadMatrix):
        """Método de eliminação de gauss com pivotagem parcial

        Formato de uma matriz (limitado a 10x10):
        * linhas separadas por `;`
        * valores separados por `,` ou whitespace
        Por exemplo, a matriz:
        ```
        1 2
        3 4
        ```
        é representada por:
        `[1 2; 3 4]` ou `[1, 2; 3, 4]`
        """
        if len(matrix) > 10 or len(matrix[0]) > 10:
            await ctx.send("Invalid Matrix Size")
            return
        if len({len(i) for i in matrix}) != 1:
            await ctx.send("Invalid Matrix Content")
            return

        await ctx.send("**Original:**\n```"
                + print_matrix(matrix)
                + "```\n**EGPP:**\n```"
                + print_matrix(gauss_solver(matrix))
                + "```")

def print_matrix(matrix):
    matrix = list(map(lambda x : list(map(str, x)), matrix))

    widths = [0] * len(matrix[0])
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            if widths[col] < len(matrix[row][col]):
                widths[col] = len(matrix[row][col]) 

    mat = ""
    for row in matrix:
        mat += '  '.join(cell.ljust(width) for cell, width in zip(row, widths)) + '\n'
    return mat

def gauss_solver(matrix):
    for i in range(len(matrix)):
        matrix = swap_pivot(matrix,i)
        for row in range(i+1, len(matrix)):
            if(matrix[i][i] != 0):
                mult = - (matrix[row][i]/matrix[i][i])
                lpivot_mult = list(map(lambda x: x * mult, matrix[i]))
                matrix[row] = [round(lpivot_mult[col] + matrix[row][col],5) for col in range(len(lpivot_mult))]
    return matrix

def swap_pivot (matrix, pos):
    # Index of the line with the biggest pivot absolute value. This line will be used for a line swap.
    max_index, value = pos, 0
    for i in range(pos, len(matrix)):
        if(abs(matrix[i][pos]) > value):
            value = abs(matrix[i][pos])
            max_index = i
    
    if(max_index != pos):
        temp = matrix[max_index]
        matrix[max_index] = matrix[pos]
        matrix[pos] = temp
    
    return matrix

def setup(bot):
    bot.add_cog(Programming(bot))     

