from twitchio.ext import commands
import requests

class Chatters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command() # Upload a list of channel chatters. Since it depends on third party API, (The hoster of this API, by the way, DOES BAN channels from his API, You should consider to use other source) It could be either unstable or inaccurate.
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def chatters(self, ctx: commands.Context, word: str = None):
        if word is None:
            channel_name = ctx.channel.name
        else:
            channel_name = word
    
        url = f"https://api.markzynk.com/twitch/chatters/{channel_name}"
        data = requests.get(url).json()

        moderators = data["chatters"].get('moderators', [])
        vips = data["chatters"].get('vips', [])
        viewers = data["chatters"].get('viewers', [])
        broadcasters = data["chatters"].get('broadcasters', [])
        
        # Get total number of chatters
        total_chatters = (
            len(moderators) +
            len(vips) +
            len(viewers) +
            len(broadcasters)
       )
        

        # Get total number of moderators
        total_moderators = (
            len(moderators)
       )

        
        # Get total number of viewers
        total_viewers = (
            len(viewers)
       )


        # Get total number of vips
        total_vips = (
            len(vips)
       )
        
        
        # Print chatter names
        chatters_list = []
        chatters_list.append(f"Chatters count: {total_chatters}\n")

        chatters_list.append(f"\nBroadcasters {len(broadcasters)}:\n")
        chatters_list.extend(broadcasters)

        chatters_list.append(f"\nModerators {len(moderators)}:\n")
        chatters_list.extend(moderators)

        chatters_list.append(f"\nVIPs {len(vips)}:\n")
        chatters_list.extend(vips)

        chatters_list.append(f"\nViewers {len(viewers)}:\n")
        chatters_list.extend(viewers)

        text = "\n".join(chatters_list)
    
        # Upload
        response = requests.post("https://paste.ivr.fi/documents", data=text, headers={"Content-Type": "text/plain"})
        if total_chatters == 0:
            await ctx.reply(f"@{word}, has no any chatters FeelsBadMan") # If there's no chatters
        else:
            if response.status_code == 200:
                key = response.json()["key"]
                link = f"https://paste.ivr.fi/{key}"
        await ctx.reply(f'» {total_chatters} chatters [{total_moderators} Moderators | {total_vips} Vips | {total_viewers} Viewers] | {link}')

def prepare(bot):
    bot.add_cog(Chatters(bot))
