from twitchio.ext import commands
import json
import datetime
import random

class Request(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def request(self, ctx, *, request_text):
        if ctx.channel.name == "vsndbot":
            now = datetime.now()
            current_time = now.strftime("%m/%d/%Y")
            id = random.randint(1, 999)
            chatter = ctx.author.name
            text = request_text
            data = {
                'name': chatter,
                'text': text,
                "time": current_time
            }
            with open('requests.json', 'r') as f:
                chat_list = f.readlines()

            with open('channels.json', 'r') as f:
                listconnected = f.readlines()

                for chat in chat_list:
                    chat_dict = json.loads(chat)

                    if chat_dict['name'] == chatter:
                        return

                for chat in listconnected:
                    connected_dict = json.loads(chat)

                    if connected_dict['name'] == chatter:
                        return

            with open('requests.json', 'a') as f:
                f.write(json.dumps(data) + '\n')
                await ctx.reply(f"Your bot request has been sent. [{chatter}: {request_text} | ID: {id}]")
        else:
            return

def prepare(bot):
    bot.add_cog(Request(bot))