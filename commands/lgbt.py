from twitchio.ext import commands
import requests
from bs4 import BeautifulSoup

class Lgbt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def lgbt(self, ctx: commands.Context, *, target: str):
        url = f"https://www.lgbtqia.wiki/wiki/{target}"
        response = requests.get(url)
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("p")
            fixed_url = url.replace(" ", "-")
            description = f"{title.get_text()}"

            await ctx.reply(f"{description:.400} | {fixed_url}")
        except (AttributeError):
            await ctx.reply(f"Cant find {target} FeelsBadMan")

def prepare(bot):
    bot.add_cog(Lgbt(bot))
