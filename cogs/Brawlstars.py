import discord
from discord.ext import commands
import brawlstats

class Brawlstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.client = client = brawlstats.Client('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkwZGYwYzVjLTI0MjItNGZiOS1hZWI3LWE4ZWE2ZmUxZWE3NSIsImlhdCI6MTY4NTc0NjAxNCwic3ViIjoiZGV2ZWxvcGVyL2VhMTI5OWYzLTNkM2QtZDEyMi1kZGUzLTg1ODQ2NjQ0YjA2ZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDcuMTUwLjIzNC44MCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.M0ve29j-RasT8k9LCvnsX7WwmXZHE82yV1gYm_l3VZNNKz9Qkr3d9I_odNqLGS_-LzoXOmOY4rtMJUKQauZ0cA', is_async=True)
    @commands.hybrid_command(help="Buy item by id", brief="Buy items")
    async def brawlstarsprofile(self, ctx, tag: str):
        """Get a brawl stars profile"""
        try:
            player = await self.client.get_profile(tag)
        except brawlstats.RequestError as e:  # catches all exceptions
            return await ctx.send('```\n{}: {}\n```'.format(e.code, e.message))  # sends code and error message
        em = discord.Embed(title='{0.name} ({0.tag})'.format(player))

        em.description = 'Trophies: {}'.format(player.trophies)  # you could make this better by using embed fields
        await ctx.send(embed=em)

async def setup(client):
    #await client.add_cog(Brawlstats(client))
    pass