import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from luke.vars import *
import time
import random

def checkconfirm(author):
    def inner_check(message):
        return message.author == author and (message.content == "y" or message.content == "n")
    return inner_check

Shopdata = {
    "Homework":{
        "Comp Sci":{
            "desc": "Comp Sci Answers",
            "items": [{"id":"codingbat","amount":2,"cost":{"dollar":3}}, {"id":"karel","cost":{"dollar":4}}, {"id":"karelclass","cost":{"dollar":2}}]
        },
        "Chemistry":{
            "desc": "Coming soon",
            "items": []
        }
    },
    "Karel":{
        "Robots": {
            "desc": "Karel J Robots",
            "items": [{"id":"urrobot","cost":{"dollar":1}}, {"id":"sorterbot","cost":{"dollar":5}}, {"id":"smartbot","cost":{"dollar":2}}]
        },
        "Objects": {
            "desc": "Walls, Beepers, and more coming soon",
            "items": [{"id":"beeper","amount":16,"cost":{"dollar":4}}]
        }
    },
    "Social":{
        "Phone Numbers": {
            "desc": "Phone Numbers",
            "items": [{"id":"numaudrey","cost":{"dollar":100}}, {"id":"num0","cost":{"codingbat":1}}]
        }
    }
}

ItemData = {
    "codingbat": {
        "name": "CodingBat",
        "desc": "A codingbat assignment answer",
        "stack": 16,
        "category": ["Shop", "Homework", "Comp Sci"]
    },
    "karel": {
        "name": "Karel Code",
        "desc": "Answer to a karel assignment(.java)",
        "stack": 8,
        "category": ["Shop", "Homework", "Comp Sci"]
    },
    "karelclass": {
        "name": "Karel Program",
        "desc": "Answer to a karel assignment(.class)",
        "stack": 12,
        "category": ["Shop", "Homework", "Comp Sci"]
    },
    "urrobot": {
        "name": "UrRobot",
        "desc": "An Instance of the UrRobot class(new UrRobot)",
        "stack": 1,
        "category": ["Shop", "Karel", "Robots"]
    },
    "smartbot": {
        "name": "SmartBot",
        "desc": "An Instance of the SmartBot class(new SmartBot)",
        "stack": 1,
        "category": ["Shop", "Karel", "Robots"]
    },
    "sorterbot": {
        "name": "SorterBot",
        "desc": "An Instance of the SorterBot class(new SorterBot)",
        "stack": 1,
        "category": ["Shop", "Karel", "Robots"]
    },
    "beeper": {
        "name": "Beeper",
        "desc": "A beeper in the karel World",
        "stack": 16,
        "category": ["Shop", "Karel", "Objects"]
    },
    "numaudrey": {
        "name": "Audrey's Phone Number",
        "desc": "Audrey's phone number",
        "stack": 1,
        "category": ["Shop", "Social", "Phone Numbers"]
    },
    "num0": {
        "name": "<redacted>'s Phone Number",
        "desc": "<redacted>'s phone number",
        "stack": 1,
        "category": ["Shop", "Social", "Phone Numbers"]
    }
}

CurrencyData = {
    "dollar": {
        "name": "Dollar",
        "desc": "1 dollar",
        "fromrate": 1,
        "torate": 1,
        "category": ["Currency"]
    },
    "token": {
        "name": "Token",
        "desc": "For the casinophil",
        "fromrate": 1200,#1200 tokens -> 1 dollar
        "torate": 1000,#1 dollar -> 1000 tokens
        "category": ["Currency"]
    }
}

def getDict(p):
            o = Shopdata
            for i in p[1:]:
                o = o[i]
            return o
def costString(cost):
    return ' + '.join([str(cost[i])+" "+i+('s' if cost[i]>1 else '') for i in cost])

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    def check(self, member):
        print("checking inventory")
        checkuser(member)
        if not "inventory" in dat[str(member.id)]:
            dat[str(member.id)]['inventory'] = []
            print(member.name+" has obtained their first item!")
    @app_commands.command()
    async def shop(self, oginteraction: discord.Interaction):
        path = ["Shop"]
        curr = getDict(path)
        def getEmbed(p):
            return discord.Embed(title=' > '.join(p), description=("Categories:\n\n"+'\n'.join([i for i in curr])) if (not 'items' in curr) else (curr["desc"]+'\n\n'+'\n'.join([str(i+1)+'. '+str(curr['items'][i]["amount"] if "amount" in curr['items'][i] else 1)+"x ["+curr['items'][i]["id"]+"] "+ItemData[curr['items'][i]["id"]]["name"]+" - "+ItemData[curr['items'][i]["id"]]["desc"]+' ('+costString(curr['items'][i]["cost"])+')' for i in range(len(curr['items']))])+"\n\nTo purchase, do **/buy <item id>**"), color=0x000000)
        ogmessage = None
        async def loadnew():
            nonlocal curr
            curr = getDict(path)
            await ogmessage.edit(embed = getEmbed(path), view = Menu(path))
        embed=getEmbed(path)
        class LegacyMenu(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.ogmessage = None
            def setmsg(self, message):
                self.ogmessage = message
            @discord.ui.button(label="Cat1", style=discord.ButtonStyle.blurple)
            async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
                print("Something")
                path.append('Cat1')
                await self.ogmessage.edit(embed = getEmbed(path))
                await interaction.response.defer()
        class ShopNavButton(discord.ui.Button):
            def __init__(self, mypath):
                super().__init__(style = discord.ButtonStyle.blurple, label = mypath)
                self.mypath = mypath
                print(mypath)
            async def callback(self, interaction: discord.Interaction):
                print("Something")
                path.append(self.mypath)
                await interaction.response.defer()
                await loadnew()
        class BackButton(discord.ui.Button):
            def __init__(self):
                super().__init__(style = discord.ButtonStyle.gray, label = "Back")
            async def callback(self, interaction: discord.Interaction):
                print("Something")
                path.pop(len(path)-1)
                await interaction.response.defer()
                await loadnew()
        class Menu(discord.ui.View):
            def __init__(self, path):
                super().__init__()
                self.value = None
                self.path = path
                if(len(path)>1):
                    self.add_item(BackButton())
                if not 'items' in curr:
                    for i in curr:
                        self.add_item(ShopNavButton(i))
        view = Menu(path)
        await oginteraction.response.send_message(embed=embed, view=view)
        ogmessage = await oginteraction.original_response()
    
    @commands.hybrid_command(help="Buy item by id", brief="Buy items")
    async def buy(self, ctx, id, amount):
        self.check(ctx.message.author)
        #if hasItems(ctx.message.author, getDict())
    '''@commands.hybrid_command(help="Buy item by id", brief="Buy items")
    async def exchange(self, ctx, amount, type, type2):
        self.check(ctx.message.author)
        if hasItems({type: amount})
        try:
            msg = await self.bot.wait_for('message', check=checkconfirm(ctx.author), timeout=10)
            if msg == 'y':
                pass#do exchange
            else:
                ctx.channel.send("Currency Exchange cancelled")
        except TimeoutError:
            ctx.channel.send("Currency Exchange tiemed out, please try again")'''
    
    @app_commands.command()
    async def exchange(self, oginteraction: discord.Interaction):
        currency1 = "dollar"
        currency2 = "dollar"
        def getCurrencyOptions():
            return [discord.SelectOption(label=i, description=CurrencyData[i]["desc"], default=i=="dollar") for i in CurrencyData]
        def getEmbed():
            return discord.Embed(title="Currency Exchange", description=costString({currency1:CurrencyData[currency1]["fromrate"]})+" > "+costString({currency1:CurrencyData[currency2]["torate"]}), color=0x000000)
        view = None
        ogmsg = None
        async def loadnew():
            await ogmsg.edit(embed = getEmbed(), view = view)
        class CurrencySelector(discord.ui.Select):
            def __init__(self, f):
                super().__init__(min_values=1,max_values=1, options=getCurrencyOptions())
                self.v = f
            async def callback(self, interaction: discord.Interaction):
                global currency1
                global currency2
                if self.v==1:
                    currency1 = self.values[0]
                else:
                    currency2 = self.values[0]
                await loadnew()
                await interaction.response.send_message("n")
        class CurrencyExchangeButton(discord.ui.Button):
            def __init__(self):
                super().__init__(label = "Exchange!", style=discord.ButtonStyle.green)
            async def callback(self, interaction: discord.Interaction):
                print(currency1+currency2)
        class Menu(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.add_item(CurrencySelector(1))
                self.add_item(CurrencySelector(2))
                self.add_item(CurrencyExchangeButton())

        view = Menu()
        embed=getEmbed()
        '''class S(discord.ui.Modal, title = "Currency Exchange"):
            def getCurrencyOptions():
                return [discord.SelectOption(label=i, description=CurrencyData[i]["desc"], default=i=="dollar") for i in CurrencyData]
            currencyone = discord.ui.Select(min_values=1, max_values=1, options = getCurrencyOptions())
            currencytwo = discord.ui.Select(min_values=1, max_values=1, options = getCurrencyOptions())
            times = discord.ui.TextInput(label = "Times", default = '1')
            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.send_message('currency exchanged!', ephemeral=True)'''
        await oginteraction.response.send_message(embed=embed, view=view)
        ogmsg = await oginteraction.original_response()
    @commands.hybrid_command(help="Get info for item", brief="Display item info")
    async def item(self, ctx: commands.Context, id):
        if(id in CurrencyData):
            dat = CurrencyData[id]
        elif(id in ItemData):
            dat = ItemData[id]
        else:
            dat = None
            await ctx.send("Item not found")
            return
        #print(getDict(dat["category"]))
        #print(dat["desc"]+"\nCategory:"+' > '.join(dat["category"][1:])+"\nCurrent cost in shop: "+costString(searchByAttr(getDict(dat["category"]), 'id', id)['cost']))
        embed = discord.Embed(title="Item: "+dat["name"]+" ["+id+"]", description=dat["desc"]+"\n**Category:** "+' > '.join(dat["category"][1:])+"\n**Current cost in shop:** "+costString(searchByAttr(getDict(dat["category"])["items"], 'id', id)['cost'])+"\n**Stacking:** "+("Unstackable" if dat["stack"]==1 else str(dat["stack"])+" per stack"))
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Shop(client))

'''@app_commands.command()
    async def shop(self, oginteraction: discord.Interaction):
        path = ["Shop"]
        def getEmbed(p):
            return discord.Embed(title=' > '.join(p), description='\n'.join([i for i in Shopdata]), color=0x000000)
        def getDict(p):
            o = Shopdata
            for i in p[1:]:
                o = o[i]
            return o
        embed=getEmbed(path)
        class ShopNavButton(discord.ui.Button):
            def __init__(self, mypath):
                super().__init__()
                self.mypath = mypath
                self.ogmessage = None
                print(mypath)
            async def callback(self, interaction: Interaction):
                print("Something")
                path.append('Cat1')
                await self.ogmessage.edit(embed = getEmbed(path))
                await interaction.response.defer()
        class Menu(discord.ui.View):
            def __init__(self, path):
                super().__init__()
                self.value = None
                self.path = path
                d = getDict(path)
                for i in d:
                    self.add_item(ShopNavButton(i))
            def setmsg(self, message):
                pass
        view = Menu(path)
        await oginteraction.response.send_message(embed=embed, view=view)
        view.setmsg(await oginteraction.original_response())'''