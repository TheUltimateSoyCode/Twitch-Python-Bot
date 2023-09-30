from twitchio.ext import commands
import json
import random
from datetime import datetime

class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def suggest(self, ctx, *, suggestion_text):
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y")
        chatter = ctx.author.name
        id = random.randint(1, 999)
        text = suggestion_text
        data = {
            'Name': chatter,
            'Text': text,
            'ID': id,
            'Date': current_time
        }

        with open('suggestions.json', 'a') as f:
            f.write(json.dumps(data) + '\n')
            emotes = ('🥺', '😳', '🤯', '🤡', '👍', '💪', '🤩', '🥳', '🤓', '😎', '😒', '😏', '😬', '🙄', 'LuL')
            emote = random.choice(emotes)
            await ctx.reply(f"Your suggestion has been sent. {emote} [{chatter}: {suggestion_text} | ID:{id}]")


def prepare(bot):
    bot.add_cog(Suggest(bot))