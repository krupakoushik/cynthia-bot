import discord
import os
from aiohttp import ClientSession
from discord.ext import commands
import aiosqlite
import requests
import openai

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_data = {}
        self.db_path = os.path.join("db", "chatbot.db")
        self.db = None

    async def create_table(self):
        self.db = await aiosqlite.connect(self.db_path)
        cursor = await self.db.cursor()
        await cursor.execute("CREATE TABLE IF NOT EXISTS chatbot (guild_id INTEGER PRIMARY KEY, channel INTEGER)")
        await self.db.commit()
        print("Table 'chatbot' created successfully")

    async def load_channel_data(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT guild_id, channel FROM chatbot") as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    guild_id, channel_id = row
                    self.channel_data[str(guild_id)] = {"channel_id": channel_id}

    async def save_channel_data(self):
        async with aiosqlite.connect(self.db_path) as db:
            for guild_id, data in self.channel_data.items():
                await db.execute("INSERT OR REPLACE INTO chatbot (guild_id, channel) VALUES (?, ?)", (guild_id, data["channel_id"]))
            await db.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()
        await self.load_channel_data()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        guild_id = str(message.guild.id)
        if guild_id not in self.channel_data:
            return

        channel_id = self.channel_data[guild_id]["channel_id"]
        if channel_id is None or message.channel.id != channel_id:
            return

        await message.channel.typing()

        googoo = message.content

        openai.api_key="Ex0N_Yeeex1_eOP7QPyy6ZtpO5n0DVE3CszJ3wDiFLU"
        openai.api_base = "https://chimeragpt.adventblocks.cc/api/v1"
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': googoo},
            ]
        )

        if 'choices' in response and len(response['choices']) > 0:
            generated_response = response['choices'][0]['message']['content']
            return await message.reply(generated_response)
        else:
            return await message.reply("I dont have any data regarding that...")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def chatbot(self, ctx, channel: discord.TextChannel):
        guild_id = str(ctx.guild.id)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT OR REPLACE INTO chatbot (guild_id, channel) VALUES (?, ?)", (guild_id, channel.id))
            await db.commit()

        self.channel_data[guild_id] = {"channel_id": channel.id}
        await self.save_channel_data()
        embed = discord.Embed(title="Chatbot channel has been successfully set to:", description=channel.mention, color=0xEBD379)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def chatbotd(self, ctx):
        guild_id = str(ctx.guild.id)

        if guild_id not in self.channel_data or self.channel_data[guild_id]["channel_id"] is None:
            return await ctx.send("Chatbot is not set in this server.")

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM chatbot WHERE guild_id=?", (guild_id,))
            await db.commit()

        self.channel_data[guild_id] = {"channel_id": None}
        await ctx.send("Chatbot has been disabled in this server.")

    def cog_unload(self):
        self.save_channel_data()
        if self.db:
            self.bot.loop.create_task(self.db.close())

async def setup(bot):
    await bot.add_cog(Chatbot(bot))
