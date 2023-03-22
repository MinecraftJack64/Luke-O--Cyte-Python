import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from luke.vars import *
import time
import random

top3 = []
def incertae(id):
    if len(top3)==0:
        top3.append(id)
        return
    if dat[str(id)]['casinophil']['tokens'] > dat[str(top3[len(top3)-1])]['casinophil']['tokens']:
        top3.append(id)
    elif dat[str(id)]['casinophil']['tokens'] < dat[str(top3[0])]['casinophil']['tokens']:
        top3.insert(0,id)
    else:
        for x in range(len(top3)):
            if dat[str(id)]['casinophil']['tokens'] < dat[str(top3[x])]['casinophil']['tokens']:
                top3.insert(x,id)
                return
        top3.append(id)
def updateleaderboard():
    top3.clear()
    for x in dat:
        if 'casinophil' in dat[x]:
            incertae(x)
            print("inserting "+x)

losses = 0
print(dat)

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    def bank(self, member):
        print("checking membership")
        if not "casinophil" in dat[str(member.id)]:
            dat[str(member.id)]['casinophil'] = {"tokens":1000,"dailycooldown":0}
            print(member.name+" has joined the casinophil!")

    @commands.hybrid_command(help="Check how many tokens you have", brief="Check how many tokens you have")
    async def tokens(self, ctx):
        member = ctx.message.author
        self.bank(member)
        await ctx.send("You have "+str(dat[str(member.id)]['casinophil']['tokens'])+" tokens")
        save_state()

    @commands.hybrid_command(help="Check how many tokens you have", brief="Check how many tokens you have")
    async def leaderboard(self, ctx):
        updateleaderboard()
        print("Leaderboard queried:\n"+"\n".join([(await self.bot.fetch_user(int(x))).name+"("+x+")" for x in top3]))
        s = ""
        for x in range(1,len(top3)+1):
            s+=str(x)+". "+(await self.bot.fetch_user(int(top3[len(top3)-x]))).name+" - "+str(dat[str(top3[len(top3)-x])]['casinophil']['tokens'])+'\n'
        embed=discord.Embed(title="LEADERBOARD", description=s, color=0x0000FF)
        await ctx.send(embed=embed)

    @commands.hybrid_command(help="Give some of your tokens to another member", brief="Donate tokens to someone")
    async def donate(self, ctx, member:discord.Member, num:int):
        donor = ctx.message.author
        self.bank(member)
        self.bank(donor)
        if num > dat[str(donor.id)]['casinophil']['tokens']:
            await ctx.send("You don't have enough")
            return
        elif num <= 0:
            await ctx.send("donate higher than 0")
            return
        dat[str(donor.id)]['casinophil']['tokens']-=num
        dat[str(member.id)]['casinophil']['tokens']+=num
        embed=discord.Embed(title="YOU DONATED TO "+member.display_name, description="They received "+str(num)+" tokens\nYou now have "+str(dat[str(member.id)]['casinophil']['tokens']), color=0x00FF00)
        await ctx.send(embed=embed)
        save_state()

    @commands.hybrid_command(help="FORBIDDEN", brief="DO NOT USE")
    async def fabricate(self, ctx, num:int):
        if True:
            await ctx.send("DO NOT CHEAT")
            return
        member = ctx.message.author
        self.bank(member)
        dat[str(member.id)]['casinophil']['tokens']+=num
        embed=discord.Embed(title="YOU CHEATED", description="You now have "+str(dat[str(donor.id)]['casinophil']['tokens']), color=0x000000)
        await ctx.send(embed=embed)
        save_state()

    @commands.hybrid_command(help="Claim a gift of 100 tokens every day", brief="Claim your daily gift")
    async def claim(self, ctx):
        member = ctx.message.author
        self.bank(member)
        if time.time()-dat[str(member.id)]['casinophil']['dailycooldown']<3600:
            embed=discord.Embed(title="YOU ALREADY CLAIMED YOUR HOURLY GIFT", description="Come back in "+str(int(3600-time.time()+dat[str(member.id)]['casinophil']['dailycooldown']))+" seconds", color=0xFFFFFF)
            await ctx.send(embed=embed)
            return
        dat[str(member.id)]['casinophil']['tokens']+=100
        dat[str(member.id)]['casinophil']['dailycooldown'] = time.time()
        embed=discord.Embed(title="YOU CLAIMED YOUR HOURLY 100 TOKEN GIFT", description="You now have "+str(dat[str(member.id)]['casinophil']['tokens'])+"\nCome back in 1h!", color=0xFFFFFF)
        await ctx.send(embed=embed)
        save_state()

    @commands.hybrid_command(help="Claim a gift of 100 tokens every day", brief="Claim your daily gift")
    async def work(self, ctx, topic):
        if topic=="math":
            base = random.randint(1,20)
            ops = []
            ops.append(random.choice(["+","-","*","/"]))
            
    @commands.hybrid_command(help="Does a coinflip to see if you lose or win", brief="Do a coinflip")
    async def toss(self, ctx):
        await ctx.send("Flipping...")
        time.sleep(random.randint(2,4))
        n = random.randint(1,50)
        if n<25:
            embed=discord.Embed(title="YOU WIN", description="Just a fun coinflip", color=0x00FF00)
        else:
            embed=discord.Embed(title="YOU LOSE", description="Just a fun coinflip", color=0xFF5733)
        await ctx.send(embed=embed)
    @commands.hybrid_command(help="Does a coinflip to see if you lose or win a bet", brief="Do a coinflip")
    async def flip(self, ctx, num:int):
        global losses
        member = ctx.message.author
        self.bank(member)
        if num > dat[str(member.id)]['casinophil']['tokens']:
            await ctx.send("You don't have enough")
            return
        elif num <= 0:
            await ctx.send("bet higher than 0")
            return
        await ctx.send("Flipping...")
        time.sleep(random.randint(2,4))
        n = random.randint(1,50)
        if n<25+losses:
            dat[str(member.id)]['casinophil']['tokens']+=num
            embed=discord.Embed(title="YOU WIN", description="You now have "+str(dat[str(member.id)]['casinophil']['tokens']), color=0x00FF00)
            losses-=1
        else:
            losses+=1
            dat[str(member.id)]['casinophil']['tokens']-=num
            embed=discord.Embed(title="YOU LOSE", description="You now have "+str(dat[str(member.id)]['casinophil']['tokens']), color=0xFF5733)
        await ctx.send(embed=embed)
        save_state()

    @commands.hybrid_command(help="Bet on roulette; types include number(0-36), color(rgb), or even or odd", brief="Play roulette")
    async def roulette(self, ctx:commands.Context, num:int, type:str, args:str = None):
        member = ctx.message.author
        self.bank(member)
        if num > dat[str(member.id)]['casinophil']['tokens']:
            await ctx.send("You don't have enough")
            return
        elif num <= 0:
            await ctx.send("bet higher than 0")
            return
        await ctx.send("Spinning...")
        time.sleep(random.randint(2,4))
        v = random.randint(0,36)
        coleur = "green" if v==0 else "red" if (1-v%2 if (v>=1 and v<=10) or (v>=19 and v<=28) else v%2)==0 else "black"
        n=False
        if type=="color":
            n=args in coleur
            
            if n and coleur=="green": num*=37
        elif type=="number":
            n=int(args)==v
            if n and v==0: num*=37
        elif type=="even" or type=="odd":
            n=(type=="even" and v%2==0) or v%2==1
        else:
            await ctx.send("not a valid bet")
            return
        dat[str(member.id)]['casinophil']['tokens']+=(num if n else num*-1)
        embed=discord.Embed(title="YOU WIN" if n else "YOU LOSE", description="You got "+coleur+" "+str(v)+"\nYou now have "+str(dat[str(member.id)]['casinophil']['tokens']), color=0xFF5733 if not n else 0x00FF00)
        print(embed)
        await ctx.send(embed=embed)
        save_state()

async def setup(client):
    await client.add_cog(Gambling(client))