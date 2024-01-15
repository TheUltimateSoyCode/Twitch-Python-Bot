from twitchio.ext import commands
import requests
import json

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("mc",)) # Get status of minecraft server 
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def minecraft(self, ctx: commands.Context, server: str):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en") # Get user language
        url = f'https://api.mcsrvstat.us/2/{server}'
        response = requests.get(url)
        data = response.json()
        # Get json data from api
        description0 = data['motd']['clean'][1]
        description1 = data['motd']['clean'][0]
        players = data['players']['online'] 
        playersmax = data['players']['max']
        ver = data['version']
        online = str(data['online'])

        message = f'{server} | Description - {description0} / {description1} | Players count - {players} ({playersmax} max) | version - {ver}, Online - {online}'
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
    bot.add_cog(Minecraft(bot))
