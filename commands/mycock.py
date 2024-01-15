from twitchio.ext import commands
import random

class Mycheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command() # ur cock
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def mycock(self, ctx: commands.Context):
        cms = random.randint(0, 500)
        await ctx.channel.send(f'@{ctx.author.name}, {cms} cm.')

def prepare(bot):
    bot.add_cog(Mycheck(bot))
