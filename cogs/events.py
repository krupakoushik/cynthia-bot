import random
from discord.ext import commands
import os
import aiosqlite
import discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.event_toggles = {}
        self.db_path = os.path.join("db", "events.db")
        self.db = None

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
    async def create_table(self):
        self.db = await aiosqlite.connect(self.db_path)
        cursor = await self.db.cursor()
        await cursor.execute(
            "CREATE TABLE IF NOT EXISTS event_toggles (guild_id INTEGER PRIMARY KEY, greetings INTEGER, no_u INTEGER, f_respects INTEGER, dad_joke INTEGER, imagine INTEGER, dead_chat INTEGER)"
        )
        await self.db.commit()
        print("Table 'event_toggles' created successfully")

    async def get_event_toggles(self, guild_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM event_toggles WHERE guild_id = ?", (guild_id,)) as cursor:
                return await cursor.fetchone()

    async def update_event_toggle(self, guild_id, event_toggles):
        async with aiosqlite.connect(self.db_path) as db:
            values = [(event, int(enabled)) for event, enabled in event_toggles.items()]
            query = f"INSERT OR REPLACE INTO event_toggles (guild_id, {', '.join(t[0] for t in values)}) VALUES (?, {', '.join('?' for _ in values)})"
            await db.execute(query, (guild_id, *(t[1] for t in values)))
            await db.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        guild_id = str(message.guild.id)
        if guild_id not in self.event_toggles:
            self.event_toggles[guild_id] = {
                "greetings": False,
                "no_u": False,
                "f_respects": False,
                "dad_joke": False,
                "imagine": False,
                "dead_chat": False
            }

        content = message.content.lower()
        event_toggles = self.event_toggles[guild_id]

        if content in ['hi', 'hello', 'yo', 'hey'] and event_toggles["greetings"]:
            greetings = [
                f'Hello {message.author.mention}! How are you today? 😄',
                f'Hey there, {message.author.mention}! What can I do for you? 🌟',
                f'Yo, {message.author.mention}! Ready for some fun? 🎉',
                f'Hiya! {message.author.mention} What\'s the latest news? 🗞️'
            ]
            reply = random.choice(greetings)
            await message.reply(reply)

        elif content == 'no u' and event_toggles["no_u"]:
            await message.reply('no u')

        elif content == 'f' and event_toggles["f_respects"]:
            await message.reply(f'{message.author.display_name} paid their respects.')

        elif content.startswith('i am') and event_toggles["dad_joke"]:
            value = message.content.split("i am ", 1)[1]
            await message.reply(f'Hello {value}, I am Dad.')

        elif content.startswith('imagine') and event_toggles["imagine"]:
            value = message.content.split("imagine ", 1)[1]
            await message.reply(f'I can\'t even imagine {value}.')

        elif content in ["dead chat", "deadchat", "ded"] and event_toggles["dead_chat"]:
            await message.reply('https://imgur.com/hh6XwIm')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def toggle(self, ctx, event_name: str):
        guild_id = ctx.guild.id
        event_name = event_name.lower()

        if event_name not in ["greetings", "no_u", "f_respects", "dad_joke", "imagine", "dead_chat"]:
            await ctx.send("Invalid event name.")
            return

        current_toggle = await self.get_event_toggles(guild_id)

        # If the guild doesn't exist in the database, insert the default values
        if not current_toggle:
            current_toggle = {"guild_id": guild_id}
            for event in ["greetings", "no_u", "f_respects", "dad_joke", "imagine", "dead_chat"]:
                current_toggle[event] = False
            await self.update_event_toggle(guild_id, current_toggle)

        # Check if the event is already enabled
        enabled = current_toggle.get(event_name, False)
        if enabled:
            await ctx.send(f"{event_name.capitalize()} event is already enabled.")
            return

        # Enable the event and update the database
        current_toggle[event_name] = True
        await self.update_event_toggle(guild_id, current_toggle)

        await ctx.send(f"{event_name.capitalize()} event has been enabled.")


    @commands.command()
    async def events(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.event_toggles:
            await ctx.send("Event toggles not initialized for this server. Please wait a moment.")
            return

        event_toggles = self.event_toggles[guild_id]
        formatted_events = "\n".join(
            [f"**{event.capitalize()}**: {'Enabled' if enabled else 'Disabled'}" for event, enabled in event_toggles.items() if event != "guild_id"]
        )

        embed = discord.Embed(title="Events:", description=formatted_events, color=0xebd379)
        embed.set_footer(text="To turn on or off, use ?toggle event_name")
        await ctx.send(embed=embed)


    def cog_unload(self):
        self.save_event_toggles()

async def setup(bot):
    await bot.add_cog(Events(bot))
