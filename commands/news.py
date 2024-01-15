from twitchio.ext import commands
import random
import requests
import json

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command() # Get latest news articles
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def news(self, ctx: commands.Context, country: str):
        api_key = '' # newsapi api key
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}'
        response = requests.get(url)
        data = response.json()

        articles = data['articles'] 
        random_article = random.choice(articles) 
        name = random_article['source']['name'] 
        title = random_article['title'] 
        emotes = ("🌏", "🌍", "🌎") # random globe
        globe = random.choice(emotes)
        message = f'📡The latest news from {country} {globe} Is: {title} . From {name}📰' # final message 

        if user_lang != "en":
            target = message
            langpair = f"en|{user_lang}"
            response = requests.get(f"https://api.mymemory.translated.net/get?q={target}&langpair={langpair}&de=v1ss0nd@yahoo.com")
            if response.status_code == 200:
                translated = response.json()["responseData"]["translatedText"]
                await ctx.reply(translated)
            else:
                await ctx.reply(f"{response.status_code}")
        else:
            await ctx.reply(message)

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

def prepare(bot):
    bot.add_cog(News(bot))
