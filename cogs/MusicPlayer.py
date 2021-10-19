import discord
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


from discord.ext.commands import Cog, Bot, command
from discord.utils import get

client = discord.Client()
bot = Bot(command_prefix="$")

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
             client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI).get_access_token(as_dict=True, check_cache=True)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope="user-modify-playback-state"))


class MusicPlayer(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.client = client

    @command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        if channel:
            await channel.connect()

    @join.error
    async def join_error(self, ctx, exc):
        if isinstance(exc, AttributeError):
            await ctx.send("You have to be connected to add Hashashin!")

    @command(pass_context=True, aliases=["disconnect"])
    async def leave(self, ctx):
        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.voice_client.disconnect(force=True)

    @leave.error
    async def leave_error(self, ctx, exc):
        if isinstance(exc.original, AttributeError):
            await ctx.send("Hashashin is not in a channel!")

    @command(pass_context=True)
    async def play(self, ctx, *, message):
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        try:
            if channel:
                await channel.connect()
        except discord.errors.ClientException:
            pass
        except:
            print("!ERROR!")

        message = "+".join(message.split())

        results = sp.search(q=message, limit=1,
                            offset=0, type='track', market=None)

        source = sp.start_playback(uris=['spotify:track:{}'.format(
            results['tracks']['items'][0]['id'])])

        url = 'https://open.spotify.com/track/{}'.format(
            results['tracks']['items'][0]['id'])

        vc.play(source)

        await ctx.send(url)

        print(url)

    @command(pass_context=True)
    async def pause(self, ctx):
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("Music has been paused.")
        else:
            await ctx.send("There is no music playing.")

    @command(pass_context=True)
    async def resume(self, ctx):

        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("Music has resumed!")
        else:
            await ctx.send("Music is not paused.")

    @command(pass_context=True)
    async def stop(self, ctx):

        vc = get(ctx.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_playing():
            vc.stop()
            await ctx.send("Music has been stopped.")
        else:
            await ctx.send("No music playing, failed to stop.")


def setup(bot):
    bot.add_cog(MusicPlayer(bot))
