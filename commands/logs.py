from twitchio.ext import commands
import requests

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def logs(self, ctx: commands.Context, *, word: str = None):
        if word is None:
            channel_name = ctx.channel.name
        else:
            channel_name = word
        fixed_name = channel_name.replace(" ", "_") 
        url = f"https://logs.raccatta.cc/?history={fixed_name}"

        await ctx.reply(f'» {url}')

def prepare(bot):
    bot.add_cog(Logs(bot))