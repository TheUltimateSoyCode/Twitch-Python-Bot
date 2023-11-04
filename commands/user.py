from twitchio.ext import commands
import requests
from datetime import datetime

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("u",))
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def user(self, ctx: commands.Context, name :str = None):
        if name is None:
            user_name = ctx.author.name
        else:
            name = name.replace ("@", "")
            name = name.replace (",", "")
            user_name = name

        url = f'https://api.ivr.fi/v2/twitch/user?login={user_name}'
        response = requests.get(url)
        data = response.json()
        format = "%Y-%m-%dT%H:%M:%S.%fZ"

        try:
            banned = data[0]['banned']
            if banned:
                chatterCount = data[0]['chatterCount']
                followers = data[0]['followers'] 
                color = data[0]['chatColor'] 
                bio = data[0]['bio']
                prefix = data[0]['emotePrefix']
                id = data[0]['id']
                display_name = data[0]['displayName']
                createdDate = data[0]['createdAt']
                banReason = data[0]['banReason']

                date_object = datetime.strptime(createdDate, format)

                output_format = "%Y-%m-%d"
                createdAt = date_object.strftime(output_format)
                
                await ctx.reply(f"{id} | @{display_name}, Created at: {createdAt} [BANNED: {banReason}😢] | Color: {color} | Prefix: {prefix} | Followers count: {followers} | Chatters count: {chatterCount} | Bio: {bio}")            
            else:
                chatterCount = data[0]['chatterCount']
                followers = data[0]['followers'] 
                color = data[0]['chatColor'] 
                bio = data[0]['bio']
                prefix = data[0]['emotePrefix']
                id = data[0]['id']
                display_name = data[0]['displayName']
                createdDate = data[0]['createdAt']
                
                date_object = datetime.strptime(createdDate, format)

                output_format = "%Y-%m-%d"
                createdAt = date_object.strftime(output_format)

                await ctx.reply(f"{id} | @{display_name}, Created at: {createdAt} | Color: {color} | Prefix: {prefix} | Followers count: {followers} | Chatters count: {chatterCount} | Bio: {bio}")
        except Exception:
            await ctx.reply(f"Cannot find {user_name} FeelsBadMan")

def prepare(bot):
    bot.add_cog(User(bot))
