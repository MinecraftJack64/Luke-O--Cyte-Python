import discord
from discord.ext import commands
import nacl
import youtube_dl
import asyncio
from youtubesearchpython import VideosSearch
import re
import lxml
from lxml import etree
import urllib
from bs4 import BeautifulSoup
import requests

def scrape_info(url):
      
    # getting the request from url
    r = requests.get(url)
      
    # converting the text
    s = BeautifulSoup(r.text, "html.parser")
      
    # finding meta info for title
    title = s.find("span", class_="watch-title").text.replace("\n", "")
      
    # finding meta info for views
    views = s.find("div", class_="watch-view-count").text
      
    # finding meta info for likes
    likes = s.find("span", class_="like-button-renderer").span.button.text
      
    # saving this data in dictionary
    data = {'title':title, 'views':views, 'likes':likes}
      
    # returning the dictionary
    return data

myvcs = []

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    @commands.hybrid_command(name='join', help="Join member's vc", invoke_without_subcommand=True)
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel")
        else:
            channel = ctx.author.voice.channel
            await channel.connect()
            myvcs.append(channel)
            print("Connected")

    @commands.command(name='checkvc', help="Temporary solution to leave empty vcs", invoke_without_subcommand=True)
    async def checkvc(self, ctx):
        for channel in myvcs:
            if len(channel.members)==1:
                voice_client = channel.guild.voice_client
                if voice_client.is_connected():
                    await voice_client.disconnect()
                    myvcs.pop(myvcs.index(channel))

    @commands.hybrid_command(help='Leave the voice channel')
    async def leave(self, ctx):
        channel = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            myvcs.pop(myvcs.index(channel))
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name='play', help='Play song')
    async def play(self, ctx,*url):
        url = ' '.join(url)
        if not '://' in url:
            def check(c):
                print(c.content)
                return ctx.message.author==c.author and c.content.isdigit() and int(c.content) > 1 and int(c.content) <= 3
            videosSearch = VideosSearch(url, limit = 3)
            rs = videosSearch.result()['result']
            await ctx.send('\n'.join([str(x+1)+". "+rs[x]["title"] for x in range(len(rs))]))
            '''msg = await self.bot.wait_for('message', check=check, timeout=30)
            if msg.author == ctx.message.author:
                url = rs[int(msg.content)-1]['link']'''
            await ctx.send("Automatically playing first option")
            url = rs[0]['link']
        try :
            server = ctx.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                print("checkpoint vc")
                filename = await YTDLSource.from_url(url, loop=self.bot.loop)
                print("checkpoint vc2")
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send('Playing {}'.format(filename))
        except Exception as e:
            await ctx.send("Not connected to a voice channel."+str(e))

    @commands.hybrid_command(name='pause', help='Pause song')
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.hybrid_command(name='resume', help='Resume song')
    async def resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.hybrid_command(name='stop', help='Stop song')
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("Not playing anything at the moment.")
    
    #@commands.Cog.listener()
    async def on_message(self, message):
        print("trigger 1")
        urls = re.findall(r'(https?://\S+)', message.content)
        print(urls)
        for x in urls:
            print("trigger 2")          
            toast = scrape_info(x)['title']
            print(toast)
            print(toast)
            if 'rick' in str(toast) or 'never gonna' in str(toast):
                print("trigger 3")
                await message.channel.send("Rickroll detected at "+x)

async def setup(client):
    await client.add_cog(Music(client))