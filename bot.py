import os
import time, random
from dotenv import load_dotenv
import discord #Imports the discord module.
from discord.ext import commands #Imports discord extensions.\
from discord.ext import tasks
from discord import app_commands
from luke.vars import *
import asyncio
#import cogs.packrat

dec = False

dms = {}

tmp = []

polls = []

#currencies = {}
#dailyclaims = {}

tmp = []
'''with open('MStat.txt', 'r') as file:
    tmp = [line.rstrip() for line in file]
    for x in tmp:
        currencies[x.split(" ")[0]] = int(x.split(" ")[1])
        incertae(x.split(" ")[0])
        dailyclaims[x.split(" ")[0]] = float(x.split(" ")[2])
        dat[x.split(" ")[0]] = {"casinophil":{"tokens":int(x.split(" ")[1]),"dailycooldown":float(x.split(" ")[2])}}
'''
with open('DMStat.txt', 'r') as file:
    tmp = [line.rstrip() for line in file]
    for x in tmp:
        dms[x.split(" ")[0]] = x.split(" ")[1]
        if not x.split(" ")[0] in dat:
            dat[x.split(" ")[0]]={}
        dat[x.split(" ")[0]]['dm'] = {"status": x.split(" ")[1]}

#print(dat)

def save_dm_state():
    f = open('DMStat.txt', 'w')
    for x in dms:
        f.write(x+" "+dms[x]+"\n")
    f.close()
save_state()
#print(dms)
#The below code verifies the "client".
def getg(n):
    ultrag = ['Alina', 'Audrey', 'Bruce', 'Jack', 'Lizzie', 'Mikayla', 'Rachel', 'Riley', 'Olric', 'Scholly', 'Stanley', 'Victor']
    g = ['Alina', 'Audrey', 'Lizzie', 'Mikayla', 'Rachel', 'Scholly', 'Maddie', 'Jason', 'Wilson', 'Justin', 'Preston', 'Max']
    fg = []
    for x in range(n):
        i = random.randrange(0, len(g))
        fg.append(g.pop(i))
    if n==1:
        return fg[0]
    elif n==2:
        return fg[0]+" and "+fg[1]
    else:
        return ', '.join(fg[:len(fg)-1])+', and '+fg[len(fg)-1]
def randstat():
    t = random.randint(1,3)
    if t==1:
        return discord.Activity(type=discord.ActivityType.watching, name=getg(random.randint(1,3)))
    elif t==2:
        return discord.Activity(type=discord.ActivityType.listening, name=getg(1))
    elif t==3:
        return discord.Game(name="with "+getg(random.randint(1,2)))
    else:
        return discord.Streaming(name=getg(random.randint(1,3)), url="")
client = commands.Bot(command_prefix='+', intents = discord.Intents.all(), activity=randstat())
@tasks.loop(minutes=2.0)
async def statsetter():
    print('changed status')
    await client.change_presence(activity=randstat())
#The below code stores the TOKEN.
load_dotenv()
botops = ["Luke O'Cyte", "Austie O'Cyte", "Lucy O'Cyte"]
print('There are currently 3 bots available to boot:'+("".join(["\n"+str(x+1)+") "+botops[x] for x in range(len(botops))])))
choise = input("Which bot do you choose? ")
TOKEN = os.getenv('DISCORD_TOKEN_'+choise)
GUILD = os.getenv('DISCORD_GUILD')
OWNER = os.getenv('DISCORD_OWNER')

start = []
end = []
cpass = []

@client.event
async def on_ready():
    print(
        f'{client.user} is connected to the following guild(s):\n'
    )
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')
        #await guild.me.edit(nick="Luke O'Cyte")
        members = '\n - '.join([str(member) for member in guild.members])
        print(f'Guild Members:\n - {members}')
    #await client.change_presence(status=":arrow_down: is gay")
    #await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="the Arcanic Anthem"))
    """activity=discord.Game('with your feelings')"""
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} commands synced")
    except Exception as e:
        print(e)
    statsetter.start()
'''
The below code displays if you have any errors publicly. This is useful if you don't want to display them in your output shell.
'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

@client.command(help="Foo", brief="Foo")
async def foo(ctx, arg):
    await ctx.send(arg)
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, I am Luke O'Cyte! Welcome to the server!(message *opt in* to interact with me in dms)"
    )
    dms[str(member.id)] = 'optout'

@client.tree.command(name="createinvite")
@app_commands.describe(uses="uses", age="age")
async def invite(interaction: discord.Interaction, age:int=0, uses:int=1):
    link = await interaction.channel.create_invite(max_age = age,max_uses = uses)
    await interaction.response.send_message(link)

@client.tree.command(name="subscribe")
@app_commands.describe(id = "id of the interaction")
async def subscribe(interaction: discord.Interaction, id:int, mypass:str=''):
    if not cpass[id-1]==mypass:
        await interaction.response.send_message("Incorrect password", ephemeral=True)
        return
    end[id-1].append(interaction.channel)
    await interaction.response.send_message("You are now subscribed", ephemeral=True)

@client.tree.command(name="unsubscribe")
@app_commands.describe(id = "id of the interaction")
async def unsubscribe(interaction: discord.Interaction, id:int):
    end[id-1].pop(end[id-1].index(interaction.channel))
    await interaction.response.send_message("You are now unsubscribed", ephemeral=True)

@client.tree.command(name="cast")
@app_commands.describe(id = "id")
async def cast(interaction: discord.Interaction, id:int, mypass:str = ''):
    start.append(interaction.channel)
    end.append([])
    cpass.append(mypass)
    await interaction.response.send_message("You are now casting to id "+str(len(start)), ephemeral=True)

@client.tree.command(name="uncast")
@app_commands.describe(id = "id")
async def uncast(interaction: discord.Interaction, id:int, mypass:str = ''):
    if cpass[id-1]==mypass:
        await interaction.response.send_message("You are no longer casting", ephemeral=True)
        start.pop(id-1)
        end.pop(id-1)
        cpass.pop(id-1)
    else:
        await interaction.response.send_message("Incorrect password", ephemeral=True)

@client.tree.command(name="nick")
@app_commands.describe(name = "Name to change to")
async def nick(interaction: discord.Interaction, name:str):
    print(OWNER)
    print(interaction.user.id)
    if str(interaction.user.id) == str(OWNER):
        await interaction.guild.me.edit(nick=name)
        await interaction.response.send_message("Nickname changed")
    else:
        await interaction.response.send_message("You can't tell me who I am!")

@client.tree.command(name="poll")
async def poll(interaction: discord.Interaction, name:str, description:str, type:str = "public", votelimit:int = -1, hidevotes:bool = False):
    votes = {'aye':0, 'nay':0}
    print(interaction.user)
    polls.append({'maker':interaction.user, 'name':name, 'description':description, 'channel':interaction.channel, 'active': True, 'type':type, 'voters':[], 'votes':votes})
    pollvalue = len(polls)-1
    polls[pollvalue]['limit'] = votelimit
    polls[pollvalue]['private'] = hidevotes
    async def close(interaction, pollvalue, type):
        if polls[pollvalue]['active']:
            if interaction.user == polls[pollvalue]['maker'] and type=='manual':
                polls[pollvalue]['active'] = False
                await interaction.response.send_message("This poll has been closed")
            else:
                await interaction.response.send_message("You do not have permission to close this poll")
            if type=='limited':
                await interaction.followup.send("The maximum votes has been reached; Poll is now closed")
        else:
            await interaction.response.send_message("This poll is already closed")
    async def vote(interaction, id, vote):
        print("Bouton clicked for poll "+str(pollvalue))
        if polls[pollvalue]['active']:
            print("Poll activity check passed")
            if interaction.user in polls[pollvalue]['channel'].members:
                if interaction.user in polls[pollvalue]['voters']:
                    await interaction.response.send_message("You already voted and this form does not allow editing")
                    return
                print("Poll permission check passed")
                polls[pollvalue]['votes'][vote] = polls[pollvalue]['votes'][vote]+1
                polls[pollvalue]['voters'].append(interaction.user)
                print("Poll "+str(pollvalue)+" has "+str(polls[pollvalue]['votes'][vote])+" aye votes")
                await interaction.response.send_message("You voted '"+vote+"'", ephemeral=polls[pollvalue]['private'])
                if polls[pollvalue]['limit']>=0 and len(polls[pollvalue]['voters'])>=polls[pollvalue]['limit']:
                    await close(interaction, pollvalue, 'limited')
            else:
                await interaction.response.send_message("You do not have permission to vote", ephemeral=True)
        else:
            await interaction.response.send_message("This pole is closed and no votes are being accepted", ephemeral=True)
    class Menu(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
        @discord.ui.button(label="Aye", style=discord.ButtonStyle.green)
        async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await vote(interaction, pollvalue, 'aye')
        @discord.ui.button(label="Nay", style=discord.ButtonStyle.red)
        async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
            await vote(interaction, pollvalue, 'nay')
        @discord.ui.button(label="Close poll", style=discord.ButtonStyle.red)
        async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
            await close(interaction, pollvalue, 'manual')
    view = Menu()
    embed=discord.Embed(title="Poll: "+name, description=description+"\nVote aye or nay. Votes are "+('private' if hidevotes else 'public'), color=0x000000)
    await interaction.response.send_message(embed=embed, view=view)

@client.event
async def on_message(message):
    global dec
    member = message.author
    if message.author == client.user:
        return
    if message.channel in start:
        for x in end[start.index(message.channel)]:
            await x.send(message.content)
    if message.author.name == "Abdullah XV" and '*' in message.content:
        pass
    if not str(member.id) in dms:
        pass
    if "Hey" in message.content and not '#' in message.content:
        await message.channel.send("Hey, "+str(message.author)+"!")
    if "gn" in message.content and len(message.content) == 2:
        await message.channel.send("Good Night!")
    if random.randint(0,10)==1 and ((str(member.id) in dat and dat[str(member.id)]['dm']['status'] == 'open') or not str(member.id) in dat):
        await member.create_dm()
        '''await member.dm_channel.send(
            f"How are you doing?"
        )'''
        dat[str(member.id)]['dm']['status'] = 'askstat'
    save_state()
    await client.process_commands(message)
'''@client.tree.command(name="roulette")
@app_commands.describe(num = "Amount to bet", type = "color, number, or even or odd", args = "A number(0-36) or color(ie. 'green' or 'g'); not needed for even/odd")
async def roulette(interaction: discord.Interaction, num:int, type:str, args:str = None):
    member = interaction.user
    bank(member)
    if num > dat[str(member.id)]['casinophil']['tokens']:
        await ctx.send("You don't have enough")
        return
    elif num <= 0:
        await ctx.send("bet higher than 0")
        return
    await interaction.response.send_message("Spinning...")
    time.sleep(random.randint(2,4))
    v = random.randint(0,36)
    coleur = "green" if v==0 else "red" if (1-v%2 if (v>=1 and v<=10) or (v>=19 and v<=28) else v%2)==0 else "black"
    n=False
    if args in ["r","g","b"]:
        args = 'red' if args == "r" else 'green' if args == "g" else 'black'
    elif not args["red","green","black"]:
        changer = await interaction.original_response()
        await changer.edit(content=args+" is not a creative color")
        return
    if type=="color":
        n=args == coleur
        
        if n and coleur=="green": num*=37
    elif type=="number":
        n=int(args)==v
        if n and v==0: num*=37
    elif type=="even" or type=="odd":
        n=(type=="even" and v%2==0) or v%2==1
    else:
        changer = await interaction.original_response()
        await changer.edit(content="not a valid bet")
        return
    dat[str(member.id)]['casinophil']['tokens']+=(num if n else num*-1)
    embed=discord.Embed(title="YOU WIN" if n else "YOU LOSE", description="You got "+coleur+" "+str(v)+"\nYou now have "+str(dat[str(member.id)]['casinophil']['tokens']), color=0xFF5733 if not n else 0x00FF00)
    print(embed)
    await (await interaction.original_response()).edit(embed=embed)
    save_state()'''
#The below code runs the bot.
#asyncio.run(bg())
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")
async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)
asyncio.run(main())
client.run(TOKEN)