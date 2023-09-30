from twitchio.ext import commands
import time
import json
import requests
import random
import psutil

start_time = time.time()

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_langs = self.load_user_langs()

    @commands.command(aliases = ("pong", "peng", "pyng", "pung", "pang"))
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def ping(self, ctx: commands.Context):
        try:
            user_info_url = f'https://api.ivr.fi/v2/twitch/user?login={ctx.channel.name}'
            user_info_response = requests.get(user_info_url)
            user_info_data = user_info_response.json()
            id = user_info_data[0]['id']

            emote_set_url = f'https://7tv.io/v3/users/twitch/{id}'
            emote_set_response = requests.get(emote_set_url)
            emote_set_data = emote_set_response.json()
            emote_set_id = emote_set_data['emote_set']['id']

            emote_url = f'https://7tv.io/v3/emote-sets/{emote_set_id}'
            emote_response = requests.get(emote_url)
            emote_data = emote_response.json()

            count = emote_data['emote_count']
            random_emote = random.randint(0, count)
            emotes = emote_data['emotes'][random_emote]['name']
            process = psutil.Process() 
            memory_usage = process.memory_info().rss 
            memory_usage_mb = memory_usage / 1024 / 1024 

            uptime = time.time() - start_time
            days, remainder = divmod(uptime, 86400)
            hours, remainder = divmod(uptime, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.user_langs = self.load_user_langs()
            user_lang = self.user_langs.get(ctx.author.name, "en")
            if user_lang != "en":
                target = f"me {emotes} Current uptime is {int(days)} days {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds | RAM Usage: {memory_usage_mb} MB |"
                langpair = f"en|{user_lang}"
                response = requests.get(f"https://api.mymemory.translated.net/get?q={target}&langpair={langpair}&de=")
                if response.status_code == 200:
                    translated = response.json()["responseData"]["translatedText"]
                    await ctx.reply(f"/{translated}")
                else:
                    await ctx.reply(f"{response.status_code}")
            else:
                await ctx.reply(f'/me {emotes} Current uptime is {int(days)} days {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds | RAM Usage: {memory_usage_mb} MB |')
                
        except Exception as e:
            await ctx.reply(f'/me pong! ({e})')

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 
    
def prepare(bot):
    bot.add_cog(Ping(bot))