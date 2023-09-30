from twitchio.ext import commands

class Pyramid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 20, commands.Bucket.user)
    async def pyramid(self, ctx: commands.Context, num: int = 3, *, target: str):
        if not ctx.author.is_mod and not ctx.author.is_vip: 
            return
        messages = []

        max_length = 500

        if ctx.author.is_mod:
            if num < 1 or num > 100:
                await ctx.reply("Pyramid cant be bigger than 100 messages")
                return
            for i in range(1, num + 1):
                message = (target + " ") * i
                if len(message) > max_length:
                    await ctx.reply("This pyramid will be bigger than 500 characters, try to reduce a scale 🤏")
                    return

        if ctx.author.is_vip:
            if num < 1 or num > 30:
                await ctx.reply("Pyramid cant be bigger than 30 messages")
                return
            for i in range(1, num + 1):
                message = (target + " ") * i
                if len(message) > max_length:
                    await ctx.reply("This pyramid will be bigger than 500 characters, try to reduce a scale 🤏")
                    return

        for i in range(1, num + 1):
            message = (target + " ") * i
            await ctx.send(message)
            messages.append(message)
            
        for message in reversed(messages[:-1]):
            await ctx.send(message)
        
def prepare(bot):
    bot.add_cog(Pyramid(bot))