from twitchio.ext import commands
import requests
from bs4 import BeautifulSoup

class Genius(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command() # Parses artists info from genius
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def genius(self, ctx: commands.Context, *, target: str):
        url = f"https://genius.com/artists/{target}"
        response = requests.get(url)
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("p")
            name = soup.find("h1")
            fixed_url = url.replace(" ", "-")
            description = f"{title.get_text()}"

            await ctx.reply(f"{name.get_text()} - {description:.400} | {fixed_url}") # Send artist info, but it could also send an error message if nothing found directly from genius website
        except (AttributeError):
            await ctx.reply(f"Cant find {target} FeelsBadMan")

def prepare(bot):
    bot.add_cog(Genius(bot))
