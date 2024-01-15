from twitchio.ext import commands
import json
import random
from datetime import datetime

class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command() # Get a request for bot addition 
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def request(self, ctx, *, suggestion_text):
        if ctx.channel.name == "vsndbot": # Works only on x channel
            now = datetime.now()
            current_time = now.strftime("%m/%d/%Y") # Time now
            chatter = ctx.author.name
            id = random.randint(1, 999) # Get a random number for id
            text = suggestion_text 
            data = {
                'Name': chatter,
                'Text': text,
                'ID': id,
                'Date': current_time
            } # Generate info that will be saved in file 

            with open('suggestions.json', 'a') as f:
                f.write(json.dumps(data) + '\n') # Save it 
                emotes = ('🥺', '😳', '🤯', '🤡', '👍', '💪', '🤩', '🥳', '🤓', '😎', '😒', '😏', '😬', '🙄', 'LuL')
                emote = random.choice(emotes)
                await ctx.reply(f"Your bot request has been sent. {emote} [{chatter}: {suggestion_text} | ID:{id}]")
        else:
            return # If it was called in other channel

def prepare(bot):
    bot.add_cog(Suggest(bot))
