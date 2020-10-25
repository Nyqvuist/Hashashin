import discord
import youtube_dl
import os
from discord.ext.commands import Cog
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot

client = discord.Client()
bot = commands.Bot(command_prefix="$")


class MusicPlayer(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = client

    @commands.command(pass_context=True)
    async def join(self, ctx):
        global vc
        channel = ctx.message.author.voice.channel
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc and vc.is_connected():
            await ctx.vc.move_to(channel)
        else:
            await channel.connect()

    @join.error
    async def join_error(self, ctx, exc):
        if isinstance(exc, AttributeError):
            await ctx.send("You have to be connected to add Hashashin!")

    @commands.command(pass_context=True, aliases=["disconnect"])
    async def leave(self, ctx):
        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.voice_client.disconnect(force=True)

    @leave.error
    async def leave_error(self, ctx, exc):
        if isinstance(exc.original, AttributeError):
            await ctx.send("Hashashin is not in a channel!")

    @commands.command(pass_context=True, aliases=["p", "P"])
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print('Removed old song file')
        except PermissionError:
            print("Trying to delete song file, but its being played.")
            await ctx.send("Theres already music playing.")
            return
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading song\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith('.mp3'):
                name = file
                print(f"Renamed file: {file}\n")
                os.rename(file, "song.mp3")

        vc.play(discord.FFmpegPCMAudio("song.mp3"),
                after=lambda e: print(f"{name} has finished playing"))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.03

        nname = name.rsplit("-", 0)
        await ctx.send(f"Playing: {nname}".format(nname))
        print("Playing")


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
