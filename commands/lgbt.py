from twitchio.ext import commands
import requests
import random
from bs4 import BeautifulSoup

class Lgbt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def lgbt(self, ctx: commands.Context, *, target:str =None):
        Genders = (
        "Digigender",
        "Amogusgender",
        "UwUgender",
        "Nyanmemegender",    
        "Bannygender",
        "Batgender",
        "Beaglegender",
        "Femboy",
        "Mechagender" ,            
        "Hardwaregender",
        "OSgender",    
        "SEGAgender",
        "Tf2gender",
        "TFPyrogender",
        "Sonigender",    
        "Twitchgender",
        "Gay",
        "Sweetgender",
        "Candygender",    
        "Breakfastgender",
        "Anonbinary",
        "Anderagin",
        "Fiumean",    
        "Sociagender",
        "Xenogender",
        "3x3gender",
        "Catgender",    
        "Glassgender",
        "Genderfluid",
        "Transgender",
        "Straight",    
        "N-Gender",
        "Neutral",
        "Neutroisflux",
        "Genderbee",    
        "Doggender",
        "Uyutsexual",
        "Bliskosexual",
        "Eshed",    
        "A-migdari",
        "Androgynos",
        "Joyfriend",
        "Homophile",    
        "Lesbian",
        "Rockgender",
        "Rapgender",
        "Weedgender",    
        "Schizic",
        "Transmasculine",
        "Fuckgender",
        "Aegosexual",    
        "Driftandrogyne",
        "Psychogender",
        "Amaxophobian",
        "Redditgender",    
        "4Changender",
        "ASMRgender",
        "Intellegender",
        "Musicagender",    
        "VOCALOIDgender",
        )
        randomgender = random.choice(Genders)
        try:
            if target is None:
                url1 = f"https://www.lgbtqia.wiki/wiki/{randomgender}"
                response1 = requests.get(url1)
                soup1 = BeautifulSoup(response1.content, "html.parser")
                title1 = soup1.find("p")
                fixed_url1 = url1.replace(" ", "-")
                description1 = f"{title1.get_text()}"

                await ctx.reply(f"{description1:.400} | {fixed_url1}")

            else:
                url = f"https://www.lgbtqia.wiki/wiki/{target}"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                title = soup.find("p")
                fixed_url = url.replace(" ", "-")
                description = f"{title.get_text()}"
                
                await ctx.reply(f"{description:.400} | {fixed_url}")
        except Exception:  
            await ctx.reply(f"Cant find {target} FeelsBadMan")

def prepare(bot):
    bot.add_cog(Lgbt(bot))
