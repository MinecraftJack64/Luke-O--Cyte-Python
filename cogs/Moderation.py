from contextvars import Context
import discord
from discord.ext import commands
from luke.vars import *
import time

censor = []

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    #The below code bans player.
    @commands.hybrid_command(help="Ban a member(admins use only)", brief="Ban a user")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send("Banned user")

    #The below code unbans player.
    @commands.hybrid_command(help="Unban a user(admins use only); Use discriminant", brief="Unban a user")
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx: commands.Context, *, member:str):
        banned_users = [entry async for entry in ctx.guild.bans(limit=2000)]
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            print("Check")
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.hybrid_command(help="Make a role", brief="Make role")
    async def createrole(self, ctx, name:str, color:str):
        guild = ctx.guild
        await guild.create_role(name=name, colour=discord.Colour(color))
        await ctx.send("Role \""+name+"\" created")

    @commands.hybrid_command(help="Make a role", brief="Make role")
    @commands.has_permissions(administrator = True)
    async def refreshguild(self, ctx: commands.Context):
        needsave = False
        if not str(ctx.guild.id) in gdat:
            gdat[str(ctx.guild.id)] = {"authedmembers":[], "lockmode":"off"}
            needsave = True
        for member in ctx.guild.members:
            if not member.id in gdat[str(ctx.guild.id)]["authedmembers"]:
                print(member.id)
                gdat[str(ctx.guild.id)]["authedmembers"].append(member.id)
                needsave = True
        if needsave:
            save_gstate()
        await ctx.send("Guild Refreshed")

    #Add a role
    @commands.hybrid_command(help="Give a role to a member(admins use only)", brief="Give role to someone")
    @commands.has_permissions(administrator = True)
    async def addrole(self, ctx: commands.Context, member : discord.Member, role : discord.Role):
        await member.add_roles(role)
        await ctx.send("Added role")
    
    @commands.hybrid_command(help="Give a role to a member(admins use only)", brief="Give role to someone")
    @commands.has_permissions(administrator = True)
    async def lockmode(self, ctx: commands.Context, mode:str):
        gdat[str(ctx.guild.id)]["lockmode"] = mode
        save_gstate()

    @addrole.error
    async def addrole_error(ctx, error):
        print(ctx)

    @commands.hybrid_command()
    async def censor(self, ctx, thing:str):
        censor.append(thing)
        await ctx.send(thing+" censored")

    @commands.hybrid_command()
    async def listcensored(self, ctx, thing:str):
        await ctx.send("All censors:\n"+'\n'.join(censor))

    @commands.hybrid_command()
    async def uncensor(self, ctx, thing:str):
        censor.remove(thing)
        await ctx.send(thing+" uncensored")

    @commands.hybrid_command()
    async def uncensorall(self, ctx):
        censor.clear()
        await ctx.send("all censors removed")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        gdat[str(guild.id)] = {}

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("test1")
        print(gdat[str(member.guild.id)]["lockmode"])
        if not member.id in gdat[str(member.guild.id)]["authedmembers"] and gdat[str(member.guild.id)]["lockmode"]=="max":
            time.sleep(5)
            print("Tried")
            await member.ban(reason="YOU have been banned by ME. HAHAHAHAHAHAHA")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        for x in censor:
            if x in message.content.lower():
                await message.delete()
                await message.channel.send("Don't use that word")

    @commands.hybrid_command()
    async def replace(self, ctx, thing:str, history:int=10000):
        messages = [message async for message in ctx.channel.history(limit=history)]
        print([m.content for m in messages])
        c = 0
        for msg in messages:
            if thing in msg.content:
                print("Edited message: "+msg.content)
                c+=1
            await msg.delete()#await msg.edit(msg.content.replace(thing, replacer))
        await ctx.send(str(c)+" message(s) deleted")
    @commands.hybrid_command()
    @commands.has_permissions(administrator = True)
    async def purge(self, ctx, frm:str, to:str, history:int=1000):
        messages = [message async for message in ctx.channel.history(limit=history)]
        #print([m.content for m in messages])
        c = 0
        delon = False
        for msg in messages:
            if frm in msg.content:
                delon = True
            if delon:
                await msg.delete()
            if to in msg.content:
                delon = False
            c+=1#await msg.edit(msg.content.replace(thing, replacer))
        await ctx.send(str(c)+" message(s) deleted")

async def setup(client):
    await client.add_cog(Moderation(client))