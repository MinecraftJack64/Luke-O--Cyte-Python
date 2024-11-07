import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = "uJV7_YDx77hP44RaAMXSMkpUolwBdQLM"
client = discord.Client(intents = discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)