from twitchio.ext import commands
import json
import requests
import random

class Pigs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.points = self.load_points()
        self.ranks = self.load_ranks()
        self.user_langs = {}


    # Soydev™ try to make a point collecting game, sometimes it works sometimes not, especially it doesnt want to count particular users. I have no idea why
    # Also they cant be separated in different cog files, it works only in one .py file
    

    @commands.command() # Get points count
    async def pigs(self, ctx: commands.Context):
        try:
            user = ctx.message.content.split()[1] # If name given - check that user's points
        except IndexError:
            user = ctx.author.name # if not then author's

        if user not in self.points: # If person who called the command has no points, then give them 10
            self.points[user] = 10

        if user not in self.ranks: # The same thing last 2 lines but with ranks
                self.ranks[user] = 1

        points = self.points[user]
        rank = self.ranks[user]

        sorted_users = sorted(self.points.items(), key=lambda x: self.ranks.get(x[0], 0), reverse=True) # Sort for showing correct place in leaderboard

        place = sorted_users.index((user, points)) + 1

        message = f'{user} {points} pigs [Rank:{rank}] Place in #top: {place}'

        await ctx.reply(message)

###
    def load_points(self):
        with open('points.json', 'r') as f:
            return json.load(f)


    def load_ranks(self):
        with open('ranks.json', 'r') as f:
            return json.load(f)
###
#




#
    @commands.command() 
    @commands.cooldown(1, 1500, commands.Bucket.user)
    async def pig(self, ctx: commands.Context):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        user = ctx.author.name
        if user not in self.points:
            self.points[user] = 5

        if user not in self.ranks:
                self.ranks[user] = 1
        random_points = random.randint(-20, 50) # Most optimal chances
        self.points[user] += random_points

        if random_points > 1: # Random lines which depends on if user got negative or positive score
            random_thing = (
            f"You just saw a few pigs near the Russian-Ukraine border and decided to take them ^", 
            "Steal few pigs🤫", "Bought some contraband pigs from Spain monkaS", "🤔 1^1 = ", 
            "I'll take them :tf: 👉 🐷 ^", 
            "🐖💨 ^"
            )
        else: # I had to change "+" to "^" because the translator api messes up everything
            random_thing = (
            f"Dead pig 💀 🐷",
            "Non-kosher meat detected DansGame", 
            "Pig is gone PoroSad",
            "Few of your pigs just ran away from you FeelsBadMan",
            "You see a random running pig and decided to caught it, but thats was a quite bad idea FeelsBadMan", 
            )      
        

        text = random.choice(random_thing)
        message = f'{text} {random_points}. | {self.points[user]} Total'
        if user_lang != "en": # If language is not default
            target = message
            langpair = f"en|{user_lang}"
            response = requests.get(f"https://api.mymemory.translated.net/get?q={target}&langpair={langpair}&de=")
            if response.status_code == 200:
                translated = response.json()["responseData"]["translatedText"]
                fixed = translated.replace("^", "+")
                await ctx.reply(fixed)
            else:
                await ctx.reply(f"{response.status_code}")
        else: 
            fixed2 = message.replace("^", "+")
            await ctx.reply(fixed2)

        self.save_points()

###
    def load_points(self):
        try:
            with open('points.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

    def save_points(self):
        with open('points.json', 'w') as f:
            json.dump(self.points, f)

    def load_ranks(self):

        try:
            with open('ranks.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

    def save_ranks(self):

        with open('ranks.json.json', 'w') as f:
            json.dump(self.ranks, f)

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
###
#




#
    @commands.command() # The same chunk of code as previous but with higher cooldown and higher points 
    @commands.cooldown(1, 3600, commands.Bucket.user)
    async def sell(self, ctx: commands.Context):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        user = ctx.author.name

        if user not in self.points:
            self.points[user] = 5
        
        random_points = random.randint(30, 400)
        self.points[user] += random_points
         

        if random_points < 150:
            random_emote = (
            f"🤣", 
            "👎", 
            "😹", 
            "😹", 
            "🐖💨",
            "🤡 ",
            "🤮",
            "🤢",
            "😢",
            "😨",
            "DansGame",
            "BibleThump",
            ":tf:",
            "haHAA",
            "peepoSad",
            )
        else: 
            random_emote = (
            f"😱",
            "😳", 
            "🙀",
            "PogBones",
            "🥰", 
            "😊", 
            "😘", 
            "😍", 
            "👍", 
            "😼",     
            "☺️", 
            "🤤", 
            "B)", 
            "EZ", 
            "peepoHappy", 
            "FeelsOkayMan", 
            )  


        emote = random.choice(random_emote)
        message = f" You've sold your old pigs and got {random_points} {emote} | {self.points[user]} Total"
        
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

###
        self.save_points()
    def load_points(self):
        try:
            with open('points.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

    def save_points(self):
        with open('points.json', 'w') as f:
            json.dump(self.points, f)

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
###
#




#
    @commands.command() # Gamble command, most of the time "breaks" balance, because even with 0.5 chance it gives too much points, consider invent fees
    @commands.cooldown(1, 2, commands.Bucket.user)
    async def bet(self, ctx: commands.Context):
        user = ctx.author.name

        if user not in self.points:
            self.points[user] = 5

        try:
            amount = int(ctx.message.content.split()[1])
        except (IndexError, ValueError): 
            await ctx.reply(f'You need to provide a valid amount of pigs')
            return

        if amount > self.points[user]: # If user has no points
            await ctx.reply(f'You dont have that many pigs to bet')
            return
        
        if amount < 1: # Actually when I first time wrote this code I didn't think about this "feature", without it person can bet negative amount and get free points
            emotes = ("FeelsBadMan", "haHAA", "FeelsWeirdMan", "FeelsDankMan", "peepoSad", "Stare")
            emote = random.choice(emotes)
            await ctx.reply(f"You can't bet nothing {emote}")
            return

        random_chance = random.random()
        if random_chance < 0.5: # Do not set chance higher than 0.5
            winnings = amount * 1
            self.points[user] += winnings
            emotes = ("Clap", "WAYTOODANK", "EZ", "AlienDance", "FeelsStrongMan", "peepoHappy", "FeelsGoodMan", ":-D", "VisLaud")
            emote = random.choice(emotes) 

            await ctx.reply(f'You bet your pigs and got {winnings} more pigs | Now you have {self.points[user]} {emote}') # if win
        else:
            self.points[user] -= amount
            emotes = ("peepoSad", "WAYTOODANK", "NotLikeThis", "FallCry", "BibleThump", "FeelsWeirdMan")
            emote = random.choice(emotes)
            await ctx.reply(f'You bet your pigs and lost them FeelsBadMan -{amount} pigs | Now you have {self.points[user]} {emote}') # if lost
        self.save_points()

###
    def load_points(self):
        try:
            with open('points.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 
        
    def save_points(self):
        with open('points.json', 'w') as f:
            json.dump(self.points, f)

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
###
#




#
    @commands.command() # An another instance of soydev™ code, completely breaks after translation. It replaces characters in usernames to not ping everyone.
    @commands.cooldown(1, 5, commands.Bucket.user)
    async def top(self, ctx: commands.Context):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        sorted_users = sorted(self.points.items(), key=lambda x: self.ranks.get(x[0], 0), reverse=True)

        message = ""

        for i in range(6):

            user = sorted_users[i][0]
            points = sorted_users[i][1]

            if user not in self.ranks:
                self.ranks[user] = 1

            rank = self.ranks[user] # List of characters
            anti_ping1 = user.replace("a", "а")
            anti_ping2 = anti_ping1.replace("e", "е")
            anti_ping3 = anti_ping2.replace("p", "р")
            anti_ping4 = anti_ping3.replace("o", "о")
            anti_ping5 = anti_ping4.replace("l", "I")
            anti_ping6 = anti_ping5.replace("v", "ѵ")
            anti_ping7 = anti_ping6.replace("k", "к")
            anti_ping8 = anti_ping7.replace("3", "Ӡ")
            anti_ping9 = anti_ping8.replace("h", "һ")
            anti_ping10 = anti_ping9.replace("j", "ј")
            anti_ping11 = anti_ping10.replace("y", "у")
            anti_ping12 = anti_ping11.replace("w", "ԝ")
            anti_ping13 = anti_ping12.replace("i", "і")
            message += f"{i+1}.{anti_ping13} - [Rank: {rank}] {points} | \n"

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

###
    def load_points(self):
        with open('points.json', 'r') as f:
            return json.load(f)


    def save_points(self):

        with open('points.json', 'w') as f:
            json.dump(self.points, f)

    def load_ranks(self):
        with open('ranks.json', 'r') as f:
               return json.load(f)

    def save_ranks(self):

        with open('ranks.json', 'w') as f:
            json.dump(self.ranks, f)

    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
###
#



#
    @commands.command() # Gives points to other person
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def give(self, ctx: commands.Context):
        sender = ctx.author.name
        if sender not in self.points:
            self.points[sender] = 10
        try:
            recipient = ctx.message.content.split()[1]
            amount = int(ctx.message.content.split()[2])
        except (IndexError, ValueError):
            await ctx.reply(f'You need to provide a valid username and amount of pigs to give')
            return

        if amount > self.points[sender]:
            await ctx.reply(f'You do not have enough pigs to give that amount')
            return

        if recipient not in self.points:
            await ctx.reply(f'This user does not exist')
            return

        self.points[sender] -= amount
        self.points[recipient] += amount

        await ctx.reply(f'You have {self.points[sender]} pigs! You gave {amount} pigs to {recipient} who now has {self.points[recipient]} pigs')
        self.save_points()

###
    def load_points(self):

        try:
            with open('points.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

    def save_points(self):
        with open('points.json', 'w') as f:
            json.dump(self.points, f)
###
#



#
    @commands.command() # Probably adds more fun, at least better than just points
    @commands.cooldown(1, 1, commands.Bucket.user)
    async def rankup(self, ctx: commands.Context):
        user = ctx.author.name

        if user not in self.points:
            self.points[user] = 10

        if user not in self.ranks:
            self.ranks[user] = 0

        points = self.points[user]

        cost = 10000
        if points < cost: # Probably better just zero balance after rankup, and make dynamic rank costs (kinda higher = more expensive)
            await ctx.reply(f'You do not have pigs to buy a rank (10000)')
            return

        self.points[user] -= cost
        self.ranks[user] += 1

        await ctx.reply(f'Now you have {self.points[user]} and [{self.ranks[user]}]')

        self.save_points()
        self.save_ranks()
###
    def load_points(self):
        try:
            with open('points.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

    def save_points(self):

        with open('points.json', 'w') as f:
            json.dump(self.points, f)

    def load_ranks(self):

        try:
            with open('ranks.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

    def save_ranks(self):

        with open('ranks.json', 'w') as f:
            json.dump(self.ranks, f)
###
def prepare(bot):
    bot.add_cog(Pigs(bot))
