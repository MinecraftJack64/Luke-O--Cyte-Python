import discord
from discord.ext import commands
import asyncio
from luke.vars import *
from datetime import datetime, timezone, timedelta
import re

class Reminder:

    def __init__(self, bot, reminder: str, end_time: datetime, destination: discord.TextChannel, author: discord.User):
        self.id = "water"#self.id = len(self.bot.reminders) + 1#Todo
        self.bot = bot
        #self.bot.reminders[self.id] = self#Todo
        self.task = None
        self.reminder = reminder
        self.end_time = end_time
        self.destination = destination if destination else author
        self.author = author
        self.task = asyncio.ensure_future(self.send_reminder())
    async def send_reminder(self):
        await discord.utils.sleep_until(self.end_time)

        embed = discord.Embed(
            title='Reminder!',
            description=self.reminder,
            color=discord.Color.green()
        )
        reminderdat = {"author": self.author, "destination": self.destination, "end_time": self.end_time, "reminder": self.destination, "status":"active"}

        if isinstance(self.destination, discord.TextChannel):
            embed.set_footer(
                text=f'Reminder sent by {self.user}'
            )

        else:
            embed.set_footer(
                text=f'This reminder is sent by you!'
            )
        try:
            await self.destination.send(
                f"**Hey {self.author.mention}!**" if isinstance(self.destination, discord.TextChannel) else None,
                embed=embed
            )

        except (discord.Forbidden, discord.HTTPException):
            pass
        await self.remove()

    async def remove(self):

        #self.bot.reminders[self.id] = None#Todo
        self.task.cancel()

    def __str__(self):
        return self.reminder
def strToTD(time_str):
    # Extract days, hours, minutes, and weeks from the string
    days = re.search(r'(\d+)\s*(?:days|d|ds|day)', time_str)
    hours = re.search(r'(\d+)\s*(?:hours|h|hrs|hs)', time_str)
    minutes = re.search(r'(\d+)\s*(?:minutes|mins|m|min)', time_str)
    weeks = re.search(r'(\d+)\s*(?:weeks|w|wk|wks|ws|week)', time_str)

    # Convert extracted time units to integers
    days = int(days.group(1)) if days else 0
    hours = int(hours.group(1)) if hours else 0
    minutes = int(minutes.group(1)) if minutes else 0
    weeks = int(weeks.group(1)) if weeks else 0

    # Return a timedelta object
    return timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
class TimeUnit:
    name: str
    seconds: int
class Time:
    unit_amount: int
    unit_name: str
    unit: TimeUnit
    seconds: int

    def __str__(self):
        return f'{self.unit_amount} {self.unit_name}'
class TimeConverter(commands.Converter):
    def get_unit(text: str) -> TimeUnit:
        text = text.lower()

        if text in ['s', 'sec', 'secs', 'second', 'seconds']:
            return TimeUnit('second', 1)
        if text in ['m', 'min', 'mins', 'minute', 'minutes']:
            return TimeUnit('minute', 60)
        if text in ['h', 'hr', 'hrs', 'hour', 'hours']:
            return TimeUnit('hour', 3600)
        if text in ['d', 'day', 'days']:
            return TimeUnit('day', 86_400)
        if text in ['w', 'wk', 'wks', 'week', 'weeks']:
            return TimeUnit('week', 604_800)
        if text in ['mo', 'mos', 'month', 'months']:
            return TimeUnit('month', 2_592_000)
        if text in ['y', 'yr', 'yrs', 'year', 'years']:
            return TimeUnit('year', 31_536_000)
        return None

    async def convert(self, _, argument: str):

        argument = argument.replace(',', '')

        if argument.lower() in ['in', 'me']: return None

        try:
            amount, unit = [re.findall(r'(\d+)(\w+)', argument)[0]][0]

            if amount == 0:
                raise commands.BadArgument('Amount can\'t be zero')

            unit = self.get_unit(unit)
            unit_correct_name = unit.name if amount == '1' else unit.name + 's'
            seconds = unit.seconds * int(amount)
        except Exception:
            raise commands.BadArgument()

        return Time(amount, unit_correct_name, unit, seconds)
class Timestuffs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    def check(self, member):
        checkuser(member)
        if not "reminders" in dat[str(member.id)]:
            dat[str(member.id)]['reminders'] = {}
            print(member.name+" checked out reminders!")
    @commands.hybrid_command(help="Send a reminder to you or a channel at a specified time or after a duration", brief="Set a reminder")
    async def remind(self, ctx: commands.Context, reminder: str, durations: commands.Greedy[TimeConverter], inorat:str="in", destination: discord.TextChannel = None):
        print("command remnd called")
        self.check(ctx.message.author)
        print("check complete")
        #convert time to a datetime
        durations = [duration for duration in durations if duration]
        durations_set = set([duration.unit for duration in durations])
        if not durations:
            await ctx.send('Durations invalid')
            return

        if len(durations) != len(durations_set):
            await ctx.send('There were duplicate units in the duration!')
            return
        total_seconds = sum([t.seconds for t in durations])
        if(inorat=="in"):
            td = timedelta(seconds=total_seconds)#strToTD(time)
            print("time delts "+td)
            end_time = datetime.now()+td
        elif(inorat=="at"):
            await ctx.send("INValid formate, 'at' not supported yet")
            #end_time = datetime.strptime(time, "%Y-%m-%d %H:%M")
        else:
            await ctx.send("INValid formate")
            return
        print("Gonna remind at "+end_time)
        rem = Reminder(self.bot, reminder, end_time, destination, ctx.message.author)
        await ctx.send("Reminder created id: "+rem.id)



async def setup(client: commands.Bot):
    await client.add_cog(Timestuffs(client))
    print("Reminders cog set up")