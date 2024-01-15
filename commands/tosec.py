from twitchio.ext import commands

class Tosec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("2secs", "2sec")) # Convert various time units to seconds
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def tosec(self, ctx: commands.Context, input: str):
        factors = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'mo': 2628000, 'y': 31540000} # known units
        for unit, factor in factors.items():
            if input.endswith(unit):
                try: # convert
                    value = float(input[:-len(unit)])
                    seconds = round(value * factor, 2)
                    await ctx.reply(f"{seconds} seconds.") # send 
                    return 
                except ValueError:
        
                    await ctx.reply(f"FeelsOkayMan 👉 use #2sec 5m/5h/5w/5mo/5y")
                    return

def prepare(bot):
    bot.add_cog(Tosec(bot))
