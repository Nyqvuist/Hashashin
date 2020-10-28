import discord
import youtube_dl
import os
import shutil
from discord.ext.commands import Cog
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot

client = discord.Client()
bot = commands.Bot(command_prefix="$")
queues = {}


class MusicPlayer(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = client
        self.queues = queues

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

        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No more songs in the queue.")
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(
                    os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("Song done, playing next song.")
                    print(f"Songs still in queue: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, "song.mp3")

                    vc.play(discord.FFmpegPCMAudio("song.mp3"),
                            after=lambda e: check_queue())
                    vc.source = discord.PCMVolumeTransformer(vc.source)
                    vc.source.volume = 0.03

                else:
                    queues.clear()
                    return

            else:
                queues.clear()

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                queues.clear()
                print('Removed old song file')
        except PermissionError:
            print("Trying to delete song file, but its being played.")
            await ctx.send("Theres already music playing.")
            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                shutil.rmtree(Queue_folder)
        except:
            print("No Queue folder.")

        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
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
                after=lambda e: check_queue())
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.03

        nname = name.rsplit("-", 0)
        await ctx.send(f"Playing: {nname}".format(nname))
        print("Playing")

    @commands.command(pass_context=True, aliases=["pa", "PAUSE"])
    async def pause(self, ctx):
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("Music has been paused.")
        else:
            await ctx.send("There is no music playing.")

    @commands.command(pass_context=True, aliases=["r", "RESUME"])
    async def resume(self, ctx):

        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("Music has resumed!")
        else:
            await ctx.send("Music is not paused.")

    @commands.command(pass_context=True, aliases=["s", "STOP"])
    async def stop(self, ctx):

        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        queues.clear()

        if vc and vc.is_playing():
            vc.stop()
            await ctx.send("Music has been stopped.")
        else:
            await ctx.send("No music playing, failed to stop.")

    @commands.command(pass_context=True, aliases=["q", "QUEUE"])
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")

        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True

        while add_queue:
            if q_num in queues:
                q_num = + 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(
            os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading song\n")
            ydl.download([url])
        await ctx.send("Adding Song" + str(q_num) + " to the queue")


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
