from twitchio.ext import commands
import openai
import requests
import json

class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ("gpt", "chat")) # Connects to a local gpt instance hosted on your pc, and most likely may be used with an official one
    @commands.cooldown(1, 40, commands.Bucket.user)
    async def ai(self, ctx, *, input):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        if len(input) > 100:
            await ctx.send(f"{ctx.author.name} 🤔 💭 (approx 2-4 minutes)")        
        else:
            await ctx.send(f"{ctx.author.name} 🤔 💭 (approx 1-2 minutes)")

        try:
            openai.api_base = "http://localhost:4891/v1"        
            prompt = f"{input}"
            model = "orca-mini-3b.ggmlv3.q4_0.bin"
            
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=90,
                temperature=0.28,
                #top_p=0.95,
                n=1,
                echo=False,
                stream=False
            )

            message = f'{response["choices"][0]["text"]}'

            if len(message) > 500:
                response = requests.post("https://paste.ivr.fi/documents", data=message)
                if response.status_code == 200:
                    key = response.json()["key"]
                    link = f"https://paste.ivr.fi/raw/{key}"
                    await ctx.reply(f'The response has exceeded the 500 characters limit. And was uploaded to: {link}')
                return
                
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

        except Exception as a:
            print(f"{a}")
            await ctx.reply(f"{a}")
        return

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

def prepare(bot):
    bot.add_cog(Gpt(bot))
