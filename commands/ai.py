from twitchio.ext import commands
import openai
import requests
import json

class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("gpt", "chat"))
    @commands.cooldown(1, 20, commands.Bucket.user)
    async def ai(self, ctx, *, input):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        await ctx.send(f"{ctx.author.name} 🤔 💭 (approx 2-3 minutes)")

        openai.api_base = ""

        prompt = f"{input}"
        model = ""
        
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=50,
            temperature=0.28,
            top_p=0.95,
            n=1,
            echo=False,
            stream=False
        )
        
        message = f'{response["choices"][0]["text"]}'

        if user_lang != "en":
            target = message
            langpair = f"en|{user_lang}"
            response = requests.get(f"https://api.mymemory.translated.net/get?q={target}&langpair={langpair}&de=")
            if response.status_code == 200:
                translated = response.json()["responseData"]["translatedText"]
                await ctx.reply(translated)
            else:
                await ctx.reply(f"{response.status_code}")
        else:
            await ctx.reply(message)   
        
    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

def prepare(bot):
    bot.add_cog(Gpt(bot))