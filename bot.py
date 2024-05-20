from twitchio.ext import commands
from datetime import datetime
from pathlib import Path
import asyncio
import json
import shutil
import subprocess

class vsndbot(commands.Bot):
    def __init__(self):
        super().__init__(token='', prefix='#', initial_channels=['']) # Token, prefix and channels

        for command in [path.stem for path in Path("commands").glob("*py")]: # Get folder with modules
            self.load_module(f"commands.{command}") # Get and import modules
            self.user_langs = {} # Local dictionary for custom language

    async def event_ready(self):
        print('Ready')
        await bot.get_channel('vsndbot').send(f"/me Reconnected") # Send message into bot chat when ready

    async def event_message(self, message): # Print messages in the terminal
        now = datetime.now() # Time
        current_time = now.strftime("%H:%M:%S") 
        try: 
            print(f"({message.channel.name}) [{current_time}] {message.author.name}: {message.content}") # Messages from regular chatters
        except AttributeError: # Since twitchio returns an error when it tries to get bot's nickname, I just hid the error message using "except"
            print(f"({message.channel.name}) [{current_time}] vsndbot: {message.content}") # Message from the bot
            return
        await self.handle_commands(message)

    async def event_command_error(self, ctx, error: Exception) -> None: # Messages when cooldown is hitten
        if isinstance(error, commands.CommandOnCooldown):
            if error.command.name == "pig":
                await ctx.reply(f"You have to wait a few minutes to catch more pigs. (Cooldown 25 minutes)")
            if error.command.name == "sell":
                await ctx.reply(f"You've sold too many pigs. Next sale in 1 hours.")


    @commands.command(aliases = ("language",)) # Set preferred language of the bot outputs
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def lang(self, ctx, lang):    
        with open("user_langs.json", "r") as f:
            self.user_langs = json.load(f)

        self.user_langs[ctx.author.name] = lang.lower()

        with open("user_langs.json", "w") as f:
            json.dump(self.user_langs, f)        
        await ctx.reply(f"Your language has been changed to {lang}")
        

    @commands.command() 
    async def dev(self, ctx: commands.Context, action, *, name: str = None):
        if ctx.author.name == "ZULUL": # Your name
            if action.startswith("reload"): # Reload module
                try:
                    self.reload_module(f'commands.{name}') 
                    await ctx.reply(f'Module "{name}" successfully reloaded')
                except Exception as e:   
                    await ctx.reply(f"{e}")
                return
                
            if action.startswith("load"): # Load module
                try:
                    self.load_module(f'commands.{name}')
                    await ctx.reply(f'Module "{name}" successfully loaded')
                except Exception as e:   
                    await ctx.reply(f"{e}")
                return

            if action.startswith("unload"): # Unload module
                try:
                    self.unload_module(f'commands.{name}')
                    await ctx.reply(f'Module "{name}" successfully unloaded')
                except Exception as e:   
                    await ctx.reply(f"{e}")
                return
            if action.startswith("cmd"): # Execute commands from chat!
                try:
                    message = subprocess.getoutput(f'{name}')
                    await ctx.reply(f"{message}")
                except Exception as e:   
                    await ctx.reply(f"{e}")
                return
        else:
            return

bot = vsndbot()
asyncio.run(bot.run())
