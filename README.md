# discord-bot
## Introduction
Just a discord bot for playing audio from files/streams handled by [youtube_dl](https://github.com/ytdl-org/youtube-dl) library and for gambling system with channel points

## Prerequisites
This bot was developed using `Python 3.7.3` version on Debian 10.<br>
Required libraries are available from the `requirements.txt` file. Type `pip install -r requirements.txt` to install.<br>
You also need to create a bot account in order to invite it to a server and generate a token. Steps can be found [here](https://discordpy.readthedocs.io/en/latest/discord.html).<br>
**Bot permissions** : *To complete*

## Basic usage
Before running the bot, you need to add your generated bot token in the `token` variable [here](https://github.com/eliasbokreta/discord-bot/blob/main/bot.py#L12).<br>
The bot is ready to run : `python3 bot.py`

## Bot owner's commands
The bot owner (the person who have registered the bot application) have some administration commands :
```
!shutdown: Disconnect the bot from the server and kill the python process running

!restart: Disconnect the bot from the server, restart the python process. This can be usefull while developing
```

## Cogs
In order to have a more comprehensive architecture, the bot is separated into multiple [*Cogs*](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html), each, representing a whole bot functionnality.
### AudioCog: `audio_cog.py`
AudioCog is a Discord voice channel based set of features. You can connect a bot to a voice channel, play local audio files, play audio from internet streams (YouTube, Dailymotion etc.. [see here](https://github.com/ytdl-org/youtube-dl)).<br>
Currently, local audio files **MUST BE** stored in `./audio` folder, and only `.mp3` extensions are supported.
Commands list :
```
!connect [channel_name]: Connect the bot to a voice channel, connect to the command author voice channel if no parameters are given.
            parameters:
                    - [channel_name]: OPTIONAL STRING Destination voice channel name.
            usage: !connect
                   !connect Channel-1

!move channel_name: Move the bot to another given voice channel, if the bot is not connected to a voice channel, the command works like !connect.
            parameters:
                    - channel_name: REQUIRED STRING Destination voice channel name.
            usage: !move Channel-2

!disconnect: Disconnect the bot from voice channel.

!stop: Stop audio from playing.

!audiofiles: List audio files available for !play command.

!play filename: Play a local audio file. If the bot is not connected to a voice channel yet, it will join the command author voice channel.
            parameters:
                    - filename : REQUIRED STRING Local audio file to play.
            usage: !play sound

!stream url: Stream audio from a given URL. If the bot is not connected to a voice channel yet, it will join the command author voice channel.
            parameters:
                    - url: REQUIRED STRING Complete URL from the stream
            usage: !stream https://www.youtube.com/watch?v=c92kd9
```

### GambleCog: `gambling_cog.py`
*To complete*

## To do
*To complete*
