import discord
import asyncio
import random
import os
import aiosqlite
from discord.ext import commands, tasks, application_checks
from discord import Interaction, ChannelType, SlashOption
from discord.abc import GuildChannel
import humanfriendly
import time as pyTime
import json

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_table(self):
        self.db = await aiosqlite.connect(self.db_path)
        cursor = await self.db.cursor()
        await cursor.execute("CREATE TABLE IF NOT EXISTS giveaway (time INTEGER, prize Text, message INTEGER, channel INTEGER, guild INTEGER, participants TEXT, winners INTEGER, finished BOOL);")
        await self.db.commit()
        print("Tables 'giveaway' created successfully")

    async def close_connection(self):
        if self.db:
            await self.db.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()





def setup(bot):
    bot.add_cog(Giveaway(bot))
