import discord
from discord.ext import commands
import aiosqlite
import os

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join("db", "prefixes.db")
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
            "CREATE TABLE IF NOT EXISTS prefixes (guild INTEGER PRIMARY KEY, prefix TEXT)"
        )
        await self.db.commit()
        print("Table 'prefixes' created successfully")

    async def close_connection(self):
        if self.db:
            await self.db.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()

    async def get_prefix(self, guild):
        async with self.db.cursor() as cursor:
            await cursor.execute(
                "SELECT prefix FROM prefixes WHERE guild = ?",
                (guild.id,),
            )
            result = await cursor.fetchone()
            return result[0] if result else "?"

    @commands.hybrid_command(with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix: str):
        async with self.db.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO prefixes (guild, prefix) VALUES (?, ?) "
                "ON CONFLICT(guild) DO UPDATE SET prefix = ?",
                (ctx.guild.id, prefix, prefix),
            )
            await self.db.commit()
            em = discord.Embed(title=f"Prefix is successfully set to `{prefix}`", color=0xEBD379)
            await ctx.send(embed=em)

    @commands.hybrid_command(with_app_command=True)
    async def prefix(self, ctx):
        prefix = await self.get_prefix(ctx.guild)
        em = discord.Embed(title=f"Prefix of {ctx.guild.name} is `{prefix}`", color=0xEBD379)
        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        async with self.db.cursor() as cursor:
            await cursor.execute(
                "DELETE FROM prefixes WHERE guild = ?",
                (guild.id,),
            )
            await self.db.commit()

async def setup(bot):
    await bot.add_cog(Prefix(bot))
