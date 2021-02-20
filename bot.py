from discord.ext import commands
import discord
import os
import sys
from audio_cog import AudioBot
from gamble_cog import GambleBot


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
token = ""


@bot.event
async def on_ready():
    print("[INFO] Bot {0} is logged in".format(bot.user))
    await bot.change_presence(activity=discord.Game('Botzer'))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.message.delete()
        await ctx.send("Command not found, please type `!help`")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Command missing required argument, please type `!help`")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.message.delete()
        await ctx.send("Command received a bad argument, please type `!help`")
    else:
        raise error


@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    """Stop the bot running [OWNER ONLY]"""
    await ctx.bot.logout()
    await ctx.message.delete()
    print("[INFO] Shutdown discord bot...")
    exit(0)


@commands.is_owner()
@bot.command()
async def restart(ctx):
    """Restart the bot [OWNER ONLY]"""
    await ctx.send("Restarting...")
    await ctx.bot.logout()
    await ctx.bot.close()
    print("[INFO] Restarting discord bot...")
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    print("[INFO] Initializing Cogs...")
    bot.add_cog(AudioBot(audio_base_dir="./audio/"))
    bot.add_cog(GambleBot())
    print("[INFO] Starting bot...")
    bot.run(token)
