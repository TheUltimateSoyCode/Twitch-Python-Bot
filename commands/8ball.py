from twitchio.ext import commands
import random
import requests
import json
import os

class Ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("8ball", "8b")) # 8 Ball
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def ball(self, ctx: commands.Context):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en") 
        folder = "data"  
        file = f"8ball.txt"
        path = os.path.join(folder, file) 
        if os.path.exists(path):
            if os.access(path, os.R_OK):
                try:
                    with open(path, "r") as f:
                        words = f.readlines()
                except Exception as e:
                    await ctx.channel.send(f"{e}")
                    return
                ball = random.choice(words)
                message = ball
        if user_lang != "en": # If default language is not English, then translate
            target = message
            langpair = f"en|{user_lang}"
            response = requests.get(f"https://api.mymemory.translated.net/get?q={target}&langpair={langpair}&de=") # Put your email after "&de=" to get higher api limits, default is 5k words per day.
            if response.status_code == 200:
                translated = response.json()["responseData"]["translatedText"]
                await ctx.reply(f"🔮 {translated}")
            else:
                await ctx.reply(f"🔮 {response.status_code}")
        else:
            await ctx.reply(f"🔮 {message}") # If English then

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

def prepare(bot):
    bot.add_cog(Ball(bot))
