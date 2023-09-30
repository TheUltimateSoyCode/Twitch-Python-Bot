from twitchio.ext import commands
import random
import requests

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def help(self, ctx: commands.Context):
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

            await ctx.reply(f"/me {emotes} 👉 https://v1ss0nd.github.io/")
        except Exception:   
            await ctx.reply(f"/me https://v1ss0nd.github.io/")

        
def prepare(bot):
    bot.add_cog(Help(bot))