from twitchio.ext import commands
import requests

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("translate",)) # Translator
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def tl(self, ctx: commands.Context):
        message = [x.strip() for x in ctx.message.content.split("|", maxsplit=2)]  # Get languages
        target = message[0][len(ctx.prefix + ctx.command.name):] 

        language = message[1] # from
        
        language1 = message[2] # to

        url = f"https://api.mymemory.translated.net/get?q={target}&langpair={language}|{language1}&de=" # Dont forget to put your (or not) email after &de= to get higher limits! 
        response = requests.get(url) 
        data = response.json()
        translatedText = data["responseData"]["translatedText"]
        
        message = f"{translatedText}"

        await ctx.reply(message) # Send translated text

def prepare(bot):
    bot.add_cog(Translate(bot))
