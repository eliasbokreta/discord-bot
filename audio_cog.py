from discord.ext import commands
import discord
import youtube_dl
from utils.utils import get_audio_files


YDL_OPTS = {'format': 'bestaudio/best',
            'extractaudio': True,
            'noplaylist': True,
            'no_warnings': True,
            'ignoreerrors': False,
            'logtostderr': True,
            'nocheckcertificate': True,
            'quiet': True}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn'}


class AudioBot(commands.Cog):
    """AudioBot handle voice channel interactions"""
    def __init__(self, audio_base_dir):
        self.channel_name = None
        self.audio_base_dir = audio_base_dir
        self.audio_files = get_audio_files(self.audio_base_dir, False)

    @commands.command()
    async def connect(self, ctx, *, channel_name: str = None):
        """Connect to a voice channel...
           Optionnal channel name can be passed as argument, otherwise
           the bot will join the message's author current voice channel
        """
        if channel_name:
            voice_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        else:
            voice_channel = ctx.author.voice.channel

        if voice_channel:
            self.channel_name = voice_channel.name
            await voice_channel.connect()
            print("[INFO] Bot connected to channel {0}".format(self.channel_name))
        await ctx.message.delete()

    @commands.command()
    async def move(self, ctx, *, channel_name: str):
        """Move the bot to another voice channel by passing the channel name as argument"""
        if ctx.voice_client:
            if discord.utils.get(ctx.guild.channels, name=channel_name):
                await ctx.voice_client.move_to(discord.utils.get(ctx.guild.channels, name=channel_name))
                print("[INFO] Bot moved to channel {0}".format(channel_name))
                self.channel_name = channel_name
            else:
                await ctx.send("Channel {0} not found".format(channel_name))
        else:
            await self.connect(ctx, channel_name=channel_name)
        await ctx.message.delete()

    @commands.command()
    async def disconnect(self, ctx):
        """Disconnect the bot from the voice channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            print("[INFO] Bot disconnected from channel {0}".format(self.channel_name))
        await ctx.message.delete()

    @commands.command()
    async def stop(self, ctx):
        """Stop the audio"""
        if ctx.voice_client.is_playing:
            ctx.voice_client.stop()
            print("[INFO] Stopped audio player")
        await ctx.message.delete()

    @commands.command()
    async def play(self, ctx, *, filename: str):
        """Play a sound using the filename
           Filenames can be retrieved with 'audiofiles' commmand
        """
        if not ctx.voice_client:
            await self.connect(ctx)
        if filename not in self.audio_files:
            await ctx.send("File {0} not found".format(filename))
        else:
            ctx.voice_client.play(discord.FFmpegPCMAudio(source="{0}{1}.mp3".format(self.audio_base_dir, filename)))
        await ctx.message.delete()

    @commands.command()
    async def audiofiles(self, ctx):
        """List all audio files available"""
        files = '"{0}"'.format('", "'.join(self.audio_files))
        await ctx.send("```Available audio files :\n{0}```".format(files))

    @commands.command()
    async def stream(self, ctx, *, url: str):
        """Stream audio from an URL"""
        if not ctx.voice_client:
            await self.connect(ctx)
        with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except youtube_dl.utils.DownloadError:
                return await ctx.send("Error, cannot play audio from this URL")
        URL = info['formats'][0]['url']
        ctx.voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.message.delete()
        await ctx.send("Playing {0}".format(url))
