from twitchio.ext import commands
import time
import requests
import random
import psutil

start_time = time.time()

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("pong", "peng", "pyng", "pung", "pang"))
    @commands.cooldown(1, 5, commands.Bucket.user)
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
            hours, remainder = divmod(uptime, 3600)
            minutes, seconds = divmod(remainder, 60)
            await ctx.reply(f'/me {emotes} Current uptime: {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds | RAM Usage: {memory_usage_mb} MB')
                
        except Exception as e:
            await ctx.reply(f'pong! Bot is up, but there is some error occurs while executing this command 👉 [{e}] ')


def prepare(bot):
    bot.add_cog(Ping(bot))
