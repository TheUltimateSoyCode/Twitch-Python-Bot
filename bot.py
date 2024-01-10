from twitchio.ext import commands
from datetime import datetime
from pathlib import Path
from git import Repo
import asyncio
import json
import shutil
import subprocess

class vsndbot(commands.Bot):
    def __init__(self):
        super().__init__(token='', prefix='#', initial_channels=[''])
        for command in [path.stem for path in Path("commands").glob("*py")]:
            self.load_module(f"commands.{command}")
            self.user_langs = {}

    async def event_ready(self):
        print('Ready')
        await bot.get_channel('vsndbot').send(f"/me Reconnected ZULULR TeaTime")

    async def event_message(self, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        try: 
            print(f"({message.channel.name}) [{current_time}] {message.author.name}: {message.content}")
        except AttributeError:
            print(f"({message.channel.name}) [{current_time}] vsndbot: {message.content}")
            return
        await self.handle_commands(message)

    async def event_command_error(self, ctx, error: Exception) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            if error.command.name == "pig":
                await ctx.reply(f"You have to wait a few minutes to catch more pigs. (Cooldown 25 minutes)")
            if error.command.name == "sell":
                await ctx.reply(f"You've sold too many pigs. Next sale in 1 hours.")

    @commands.command(aliases = ("language",))
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
        if ctx.author.name == "v1ss0nd":
            token = ""
            if action.startswith("reload"):
                try:
                    self.reload_module(f'commands.{name}')
                    await ctx.reply(f'Module "{name}" successfully reloaded')
                except Exception as e:   
                    await ctx.reply(f"{e}")
                return
                
            if action.startswith("load"):
                try:
                    self.load_module(f'commands.{name}')
                    await ctx.reply(f'Module "{name}" successfully loaded')
                except Exception as e:   
                    await ctx.reply(f"{e}")
                return

            if action.startswith("unload"):
                try:
                    self.unload_module(f'commands.{name}')
                    await ctx.reply(f'Module "{name}" successfully unloaded')
                except Exception as e:   
                    await ctx.reply(f"{e}")
                return
            
            if action.startswith("clone"):
                try:
                    repo_url = f"https://{token}:x-oauth-basic@github.com/v1ss0nd/vsndbot"
                    repo = Repo.clone_from(repo_url, "./temp")
                    Path(f"./temp/{name}").rename(f"./{name}")
                    shutil.rmtree("./temp")
                    await ctx.reply(f'File "{name}" successfully cloned from ./v1ss0nd/vsndbot/{name}')
                except Exception as e:   
                    await ctx.reply(f"{e}")
                return
            if action.startswith("cmd"):
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
