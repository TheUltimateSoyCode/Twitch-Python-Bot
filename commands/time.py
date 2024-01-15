from twitchio.ext import commands
import requests
from datetime import datetime

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command() # Get current time in particular city
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def time(self, ctx: commands.Context, region :str, city :str):
      url = f"http://worldtimeapi.org/api/timezone/{region}/{city}"
      response = requests.get(url)
      data = response.json()

      time = data['datetime']
      place = data['timezone']

      utc_dt = datetime.fromisoformat (time)

      normal_dt = utc_dt.strftime ("%A, %H:%M:%S") # Convert to normal, human readable format

      await ctx.reply(f"Time in {place} - {normal_dt}")

def prepare(bot):
    bot.add_cog(Time(bot))
