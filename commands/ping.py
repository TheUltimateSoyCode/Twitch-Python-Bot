from twitchio.ext import commands
import time
start_time = time.time()

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("pong", "peng", "pyng", "pung", "pang"))
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def ping(self, ctx: commands.Context):
        try:
            uptime = time.time() - start_time
            hours, remainder = divmod(uptime, 3600)
            minutes, seconds = divmod(remainder, 60)
            await ctx.reply(f'/me 🥱 {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds')
        except Exception as e:
            await ctx.reply(f'pong! [{e}] ')


def prepare(bot):
    bot.add_cog(Ping(bot))
