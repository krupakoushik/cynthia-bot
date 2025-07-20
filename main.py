import discord
from dotenv import load_dotenv
import os
import asyncio
import sys
import traceback
from discord.ext import commands, tasks
import itertools
from discord.ext.commands import clean_content, has_permissions, MissingPermissions
import random
import logging
import json
import aiosqlite
from discord import Game, ActivityType

load_dotenv()

logging.basicConfig(level=logging.INFO)

async def get_prefix(bot, message):
    if not message.guild:
        return "?"

    async with aiosqlite.connect("db/prefixes.db") as db:
        cursor = await db.execute(
            "SELECT prefix FROM prefixes WHERE guild = ?",
            (message.guild.id,),
        )
        result = await cursor.fetchone()
        return result[0] if result else "?"

activities = [
    {"type": discord.ActivityType.playing, "name": "hide and seek with commands!"},
    {"type": discord.ActivityType.playing, "name": "fetch with data. Woof!"},
    {"type": discord.ActivityType.playing, "name": "a sneaky game of Among Us!"},
    {"type": discord.ActivityType.playing, "name": "the role of a wise fortune teller."},
    {"type": discord.ActivityType.playing, "name": "\"Count to 1000\" with the community."},
    {"type": discord.ActivityType.playing, "name": "detective, solving server mysteries."},
    {"type": discord.ActivityType.playing, "name": "rock-paper-scissors with users!"},
    {"type": discord.ActivityType.playing, "name": "mind games with Discord API."},
    {"type": discord.ActivityType.playing, "name": "\"Bot Olympics\" behind the scenes."},
    {"type": discord.ActivityType.playing, "name": "\"Guess the command\" game!"},
    {"type": discord.ActivityType.playing, "name": "tag with other bots. Catch me if you can!"},
    {"type": discord.ActivityType.playing, "name": "\"Bot-ception\" within servers."},
    {"type": discord.ActivityType.watching, "name": "movies with friends!"},
    {"type": discord.ActivityType.watching, "name": "you waste away your life."},
    {"type": discord.ActivityType.watching, "name": "the stars in the night sky."},
    {"type": discord.ActivityType.listening, "name": "your favorite tunes."},
    {"type": discord.ActivityType.listening, "name": "the raindrops on the window."},
    {"type": discord.ActivityType.listening, "name": "one direction"},
    {"type": discord.ActivityType.listening, "name": "heart-wrenching music"},
]

random.shuffle(activities)
activity_cycle = itertools.cycle(activities)

bot = commands.Bot(
    command_prefix=get_prefix,
    owner_ids=[730634576321314867],
    intents=discord.Intents.all(),
    case_insensitive=True
)
bot.remove_command('help')


async def main():
    for file in os.listdir('cogs'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{file[:-3]}')
                print(f'{file} cog is working!')
            except Exception as e:
                print(e)
    TOK = os.getenv("DISCORD_TOKEN")
    await bot.start(TOK)
    
@bot.command()
@commands.is_owner()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Done!")

@tasks.loop(minutes=10)
async def change_status():
    activity = next(activity_cycle)
    await bot.change_presence(activity=discord.Activity(type=activity["type"], name=activity["name"]))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    change_status.start()

@bot.command()
@commands.is_owner()
async def servers(ctx):
    guilds = bot.guilds
    server_list = "\n".join(f"{i+1}. {guild.name} (ID: {guild.id}) (Members: {guild.member_count})" for i, guild in enumerate(guilds))
    embed = discord.Embed(title="List of Servers", description=server_list, color=0xEBD379)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def leaveguild(ctx, *, guild_name: str):
    guild = discord.utils.get(bot.guilds, name=guild_name)
    if guild:
        await guild.leave()
        await ctx.send(f"I left the server: {guild.name} (ID: {guild.id})")
    else:
        await ctx.send("I couldn't find the specified server.")

@bot.command()
@commands.is_owner()
async def getinvite(ctx, *, guild_name: str):
    guild = discord.utils.get(bot.guilds, name=guild_name)
    if guild:
        try:
            invite = await guild.text_channels[0].create_invite(max_age=86400)
            await ctx.send(f"Invite link for {guild.name}: {invite}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to create an invite for that server.")
    else:
        await ctx.send("I couldn't find the specified server.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="⛔ Insufficient Permissions", description="You don't have the necessary permissions to use this command.", color=0xebd379)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="🕒 Command Cooldown", description=f"Oops! This command is on cooldown. Please try again in **{error.retry_after:.0f}** seconds.", color=0xebd379)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="❓ Command Not Found", description="No command under that name is found.", color=0xebd379)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)

        embed = discord.Embed(title="❗ Command Usage", color=0xEBD379)
        embed.add_field(name="Correct Usage", value=f"`{ctx.prefix}{helper} {ctx.command.signature}`")
        embed.add_field(name="Example", value=f"`{ctx.prefix}{helper} {ctx.command.usage}`")
        embed.set_footer(text="Make sure to replace <> with the actual values.")

        await ctx.send(f"{ctx.author.mention} The correct way of using that command is:", embed=embed)
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())
