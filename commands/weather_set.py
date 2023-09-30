from twitchio.ext import commands
import requests
import json

class Weather_set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_langs = self.load_user_langs()

    @commands.command()
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def set(self, ctx: commands.Context, city: str):
        with open("locations.json", "r") as f:
            locations = json.load(f)

        user_id = ctx.author.id
        locations[user_id] = city

        with open("locations.json", "w") as f:
            json.dump(locations, f)
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        message = f'Your location has been set to {city} .'
        if user_lang != "en":
            target = message
            langpair = f"en|{user_lang}"
            response = requests.get(f"https://api.mymemory.translated.net/get?q={target}&langpair={langpair}&de=")
            if response.status_code == 200:
                translated = response.json()["responseData"]["translatedText"]
                await ctx.reply(translated)
            else:
                await ctx.reply(f"{response.status_code}")
        else:
            await ctx.reply(message)

    def load_locations(self):

        try:
            with open('locations.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

    def save_locations(self):
        with open('locations.json', 'w') as f:
            json.dump(self.locations, f)

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

def prepare(bot):
    bot.add_cog(Weather_set(bot))