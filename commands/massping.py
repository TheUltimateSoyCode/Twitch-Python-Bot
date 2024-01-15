from twitchio.ext import commands
import random
import requests

class Massping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command() # Ping everyone in the channel (very fun and cool command fr)
    @commands.cooldown(1, 20, commands.Bucket.user)
    async def massping(self, ctx: commands.Context, count: int=None, *, word=None):
        if not ctx.author.is_mod: # If not mod - ignore, but you can either remove or change it to ctx.author.is_vip
            return

        if ctx._bot_is_mod() is False: # Ask nicely for a mod
            await ctx.reply("The bot requires a mod to execute this command") 
            return

        if count is None: # If you want to do it by yourself
            chatters = list(ctx.channel.chatters) # Here it uses a twitch chatters endpoint (or smth) that works like a shit, but using third party API in this case would be pretty bad (in case of usage, since it makes a new request every time when the command ia being called)
            nicknames = [user.name for user in chatters]
            text = '\n'.join(nicknames) 
            response = requests.post("https://paste.ivr.fi/documents", data=text) # Upload
            if response.status_code == 200:
                key = response.json()["key"]
                link = f"https://paste.ivr.fi/{key}"
                await ctx.reply(f':tf: 🤜 🔔 {link}') # Send link with chatters list
                return

        for i in range(count): # Loop for x times
            if ctx.author.is_mod:
                if count < 1 or count > 100: # If count is more than 100 = ignore
                    return
            chatters_list = list(ctx.channel.chatters)
            random_chatter = random.choice(chatters_list)
            random_chatter_name = random_chatter.name
            emotes = ('🥺', '😍', '😂', '😱', '😳', '🤯', '😤', '🤢', '🤡', '👻', '😿', '😹', 'Stare', 'peepoHappy', 'ApuApustaja', 'FeelsOkayMan', 'FeelsStrongMan', 'FeelsWeirdMan', 'FeelsDankMan', 'gachiGASM', 'Gayge', 'bUrself', '4Head', '💀', '☠️', '🤩', '🥳', '🤓', '😎', ':tf:','😒', '😏', '😬', '🙄', 'AlienDance', 'VisLaud', 'LuL', 'KKona') # List of emotes
            emote = random.choice(emotes)
            if word is None:             
                await ctx.send(f'{emote} 🤜 🔔 {random_chatter_name}') # If command was called without "word" 
            else:             
                await ctx.send(f'{random_chatter_name} {word}') # If it was called with "word"

def prepare(bot):
    bot.add_cog(Massping(bot))
