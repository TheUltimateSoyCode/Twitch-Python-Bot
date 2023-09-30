from twitchio.ext import commands
import requests

class Def(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("def","dict","meaning"))
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def dictionary(self, ctx: commands.Context, word : str):
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        response = requests.get(url)
        data = response.json()

        try:
            word = data[0]['word']
            meaning = data[0]['meanings'][0]['definitions'][0]['definition']
            meaning2 = data[0]['meanings'][0]['definitions'][1]['definition']
            url = data[0]['sourceUrls'][0]

        except KeyError:
           url = "123"

        if url == "123":
            message = f'I cant find this word.'
        else:
            message = f'{word} — {meaning}. Or — {meaning2} | {url} '

        await ctx.reply(message)

def prepare(bot):
    bot.add_cog(Def(bot))