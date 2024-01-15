from twitchio.ext import commands
import asyncio

class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command() # Spam
    @commands.cooldown(1, 15, commands.Bucket.user)
    async def spam(self, ctx: commands.Context, count: int, *, message :str=None):
        if not ctx.author.is_mod and not ctx.author.is_vip: 
            return    
            
        if ctx._bot_is_mod() is False:
            await ctx.reply("The bot requires a mod to execute this command") # Ask nicely for a mod
            return

        max_countMod = 100 # Maximum count of messages for mod
        max_countVip = 30 # Maximum count of messages for vip

        if ctx.author.is_mod: 
            if count > max_countMod:
                await ctx.reply(f"100 message limit FeelsBadMan")
                return

        if ctx.author.is_vip:
            if count > max_countVip:
                await ctx.reply(f"30 message limit for vips FeelsBadMan")
                return

        if ctx.author.is_mod:
            for i in range(count):
                await ctx.send(message)

        if ctx.author.is_vip:
            for i in range(count):
                await ctx.send(message)
                await asyncio.sleep(0.2) # vip's spam is slightly slower

def prepare(bot):
    bot.add_cog(Spam(bot))
