from twitchio.ext import commands
import requests
import pyfiglet

class Ascii(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command() # Creates an ascii art, works as shit, and looks ok only in paste.ivr.fi, if you try to paste it to chat or somewhere else it wont look nice at all
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def ascii(self, ctx: commands.Context):
        args = ctx.message.content.split()
        if len(args) > 1: # Get text
            text = args[1]
            if len(args) > 2: # Get style
                style = args[2]
            else:
                style = "standard" # Full list of styles you can find on pyfiglet docs
            ascii = pyfiglet.figlet_format(text, font=style)
            fixed = ascii.replace(" ", "_") # You can remove it if you dont like how it looks, but at least it tries to fix broken spaces when you copying it.
            response = requests.post("https://paste.ivr.fi/documents", data=fixed)
            if response.status_code == 200:
                key = response.json()["key"]
                link = f"https://paste.ivr.fi/{key}"
                await ctx.reply(f"{link}")
            else:
                await ctx.reply(f"{response.status_code}")
        else:
            await ctx.reply("FeelsOkayMan 👉 #ascii [text] [style], (available styles = slant, 3-d, 3x5, 5lineoblique, alphabet, banner3-D, doh, standard, isometric1, letters, alligator, dotmatrix)")

def prepare(bot):
    bot.add_cog(Ascii(bot))
