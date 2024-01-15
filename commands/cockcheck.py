from twitchio.ext import commands
import os
import random
import requests
import json

class Cockcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command() # Chooses random chatter from viewers list and gives a random percent
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def cockcheck(self, ctx: commands.Context, *, word=None):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        folder = "data"
        file = f"cock.txt"
        path = os.path.join(folder, file)
        if os.path.exists(path):
            if os.access(path, os.R_OK):
                try:
                    with open(path, "r") as f:
                        words = f.readlines()
                except Exception as e:
                    await ctx.channel.send(f"@{ctx.author.name},{e}")
                    return
                cock = random.choice(words)
        emotes = ('🥺', '😍', '😂', '😱', '😳', '🤯', '😤', '🤢', '🤡', '👻', '👎', '👍', '😿', '😹', '💪', '💀', '☠️', '🤩', '🥳', '🤓', '😎', ':tf:','😒', '😏', '😬', '🙄', 'AlienDance', 'VisLaud', 'LuL', 'KKona')
        emote = random.choice(emotes)
        chatters_list = list(ctx.channel.chatters)
        random_chatter = random.choice(chatters_list)
        random_chatter_name = random_chatter.name
        if word is None:             
            message = f'{ctx.author.name} Checks {random_chatter_name} cock... {cock} {emote}'
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
        else:             
            message = f'{ctx.author.name} Checks {word} cock... {cock} {emote}'
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
        
    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        
def prepare(bot):
    bot.add_cog(Cockcheck(bot))
