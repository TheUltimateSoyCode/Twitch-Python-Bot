from twitchio.ext import commands

class Pyramid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command() # A pyramid, if your bot doesn't have a verification, change the limit from 100 to 30 or 50.
    @commands.cooldown(1, 25, commands.Bucket.user)
    async def pyramid(self, ctx: commands.Context, num: int = 3, *, target: str):
        if not ctx.author.is_mod and not ctx.author.is_vip: 
            return
        messages = []

        if ctx.author.is_mod:
            if num < 1 or num > 100:
                await ctx.reply("Pyramid cant be bigger than 100 messages")
                return

        if ctx.author.is_vip:
            if num < 1 or num > 30:
                await ctx.reply("Pyramid cant be bigger than 30 messages")
                return

        for i in range(1, num + 1):
            message = (target + " ") * i
            await ctx.send(f"{message:.500}") # Because twitchio returns an error if message larger than 500.
            messages.append(f"{message:.500}")
            
        for message in reversed(messages[:-1]):
            await ctx.send(f"{message:.500}")
        
def prepare(bot):
    bot.add_cog(Pyramid(bot))
