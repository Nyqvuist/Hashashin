import hikari
import tanjun
import lavasnek_rs
import typing

music = tanjun.Component()


async def _join_voice(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> typing.Optional[hikari.Snowflake]:
    assert ctx.guild_id is not None

    if ctx.client.cache and ctx.client.shards:
        if (voice_state := ctx.client.cache.get_voice_state(ctx.guild_id, ctx.author)) is None:
            await ctx.respond("You have to be connected to a voice channel!")
            return None

        await ctx.client.shards.update_voice_state(ctx.guild_id, voice_state.channel_id, self_deaf=True)
        conn = await lavalink.wait_for_full_connection_info_insert(ctx.guild_id)
        await lavalink.create_session(conn)
        return voice_state.channel_id

    return None


@music.with_slash_command
@tanjun.with_str_slash_option("song", "Song title or youtube link.")
@tanjun.as_slash_command("play", "Play a song, or add to queue.")
async def play_as_slash(ctx: tanjun.abc.SlashContext, song: str, lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),) -> None:
    await _play_track(ctx, song, lavalink)


async def _play_track(ctx: tanjun.abc.Context, song: str, lavalink: lavasnek_rs.Lavalink) -> None:
    assert ctx.guild_id is not None

    conn = await lavalink.get_guild_gateway_connection_info(ctx.guild_id)

    if not conn:
        if not await _join_voice(ctx, lavalink):
            return

    if not (tracks := (await lavalink.auto_search_tracks(song)).tracks):
        await ctx.respond(f"No tracks found the song: <{song}>")
        return

    try:
        await lavalink.play(ctx.guild_id, tracks[0]).requester(ctx.author.id).queue()

    except lavasnek_rs.NoSessionPresent:
        await ctx.respond("Unable to join voice. This may be an internal issue.")
        return

    await ctx.respond(f"Added to queue: `{tracks[0].info.title}`")


@music.with_slash_command
@tanjun.as_slash_command("skip", "Skips the current song.")
async def skip_as_slash(ctx: tanjun.abc.SlashContext, lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),) -> None:
    await _skip_track(ctx, lavalink)


async def _skip_track(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
    assert ctx.guild_id is not None

    if not (skip := await lavalink.skip(ctx.guild_id)):
        await ctx.respond("No tracks to skip.")
        return
    elif node := await lavalink.get_guild_node(ctx.guild_id):
        if not node.queue and not node.now_playing:
            await lavalink.stop(ctx.guild_id)

    await ctx.respond(f"Skipped: {skip.track.info.title}")


@music.with_slash_command
@tanjun.as_slash_command("stop", "Stops the currently playing song, skip to play again.")
async def stop_as_slash(
    ctx: tanjun.abc.SlashContext,
    lavalink: lavasnek_rs.Lavalink = tanjun.injected(
        type=lavasnek_rs.Lavalink),
) -> None:
    await _stop_playback(ctx, lavalink)


async def _stop_playback(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
    assert ctx.guild_id is not None

    await lavalink.stop(ctx.guild_id)
    await ctx.respond("Stopped playback.")


@music.with_slash_command
@tanjun.as_slash_command("leave", "Leaves the voice channel and clears the queue.")
async def leave_as_slash(
    ctx: tanjun.abc.SlashContext,
    lavalink: lavasnek_rs.Lavalink = tanjun.injected(
        type=lavasnek_rs.Lavalink),
) -> None:
    await _leave_voice(ctx, lavalink)


async def _leave_voice(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
    assert ctx.guild_id is not None

    if await lavalink.get_guild_gateway_connection_info(ctx.guild_id):
        await lavalink.destroy(ctx.guild_id)

        if ctx.client.shards:
            await ctx.client.shards.update_voice_state(ctx.guild_id, None)
            await lavalink.wait_for_connection_info_remove(ctx.guild_id)

        await lavalink.remove_guild_node(ctx.guild_id)
        await lavalink.remove_guild_from_loops(ctx.guild_id)

        await ctx.respond("Disconnected from voice.")
        return

    await ctx.respond("I am not currently connected.")


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(music.copy())
