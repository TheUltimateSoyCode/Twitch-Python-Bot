from twitchio.ext import commands
import requests
import json
import os

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_langs = self.load_user_langs()

    @commands.command(aliases = ("погода", "w")) # Weather
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def weather(self, ctx: commands.Context, city: str = None):
        api_key = '' # API Key
        with open("locations.json", "r") as f:
            locations = json.load(f)
        if city is None: # If no city given
            user_id = ctx.author.id
            if user_id in locations: # Check if user has their city saved
                city = locations[user_id]
            else: # If no
                await ctx.reply(f'Please provide a city name or use #set to save your location.')
                return
        self.user_langs = self.load_user_langs() # Get user language
        user_lang = self.user_langs.get(ctx.author.name, "en")
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang={user_lang}' # URL With custom city and language
        response = requests.get(url)
        data = response.json()

        if data['cod'] != 200: 
            await ctx.reply(f'Sorry, I could not find the weather for {city}.') # If city does not exist or the api is down
            return
        # Get json data
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        cloudscover = data['clouds']['all']
        pressure = data['main']['pressure']
        description = data['weather'][0]['description']
        name = data['name']
        #

        message = f'Current weather in {name} is: {description} 🌤. Temperature {temp}°C, feels like {feels_like}°C. Humidity {humidity}%. Air pressure: {pressure}hPa. Cloud cover {cloudscover}%.  Wind speed {wind_speed} m/s.'
        if user_lang != "en": # if language not default (eng)
            target = message
            langpair = f"en|{user_lang}"
            response = requests.get(f"https://api.mymemory.translated.net/get?q={target}&langpair={langpair}&de=")
            if response.status_code == 200:
                translated = response.json()["responseData"]["translatedText"]
                await ctx.reply(translated)
            else: # If translation api is down
                await ctx.reply(f"{response.status_code}")
        else: # If default
            await ctx.reply(message)

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

def prepare(bot):
    bot.add_cog(Weather(bot))
