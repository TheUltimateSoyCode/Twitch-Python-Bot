from twitchio.ext import commands
import requests
from bs4 import BeautifulSoup

class Wiktionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ("def","dict","meaning"))
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def dictionary(self, ctx: commands.Context, language, *, search : str =None):
        try:
            if search is None:
                url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{language}'
                response = requests.get(url)
                data = response.json()

                word = data[0]['word']
                meaning = data[0]['meanings'][0]['definitions'][0]['definition']
                meaning2 = data[0]['meanings'][0]['definitions'][1]['definition']

                message = f'{word} — {meaning}. Or — {meaning2}'

                await ctx.reply(message)
                return

            url = f"https://{language}.wiktionary.org/wiki/{search}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            word1 = soup.find("p")
            word2 = soup.find("h1")
            meaning1 = soup.find("ol")
                                     
            await ctx.reply(f"{word2.get_text()} ({word1.get_text()}) — {meaning1.get_text():.400}")
        except Exception as a:
            print(f"{a}")
            await ctx.reply(f"Cant find the meaning FeelsBadMan")

def prepare(bot):
    bot.add_cog(Wiktionary(bot))
