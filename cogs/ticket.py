import discord
from discord.ext import commands
import aiosqlite
import os
import asyncio

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join("db", "tickets.db")
        self.db = None

    async def create_table(self):
        self.db = await aiosqlite.connect(self.db_path)
        cursor = await self.db.cursor()
        await cursor.execute(
                "CREATE TABLE IF NOT EXISTS ticket_configs (guild_id INTEGER PRIMARY KEY, msg_id INTEGER, category_id INTEGER)"
        )
        await self.db.commit()
        print("Table 'ticket' created successfully")

    async def close_connection(self):
        if self.db:
            await self.db.close()

    async def save_ticket_config(self, guild_id, msg_id, category_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO ticket_configs (guild_id, msg_id, category_id) VALUES (?, ?, ?)",
                (guild_id, msg_id, category_id),
            )
            await db.commit()

    async def get_ticket_config(self, guild_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT msg_id, category_id FROM ticket_configs WHERE guild_id = ?",
                (guild_id,),
            )
            return await cursor.fetchone()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        config = await self.get_ticket_config(payload.guild_id)

        if config is None:
            return

        ticket_emoji = "\U0001F3AB"
        if payload.message_id == int(config[0]) and str(payload.emoji) == ticket_emoji:
            category = guild.get_channel(int(config[1]))
            if category is None:
                return

            member = guild.get_member(payload.user_id)
            if member is None:
                return

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True),
            }

            channel = await guild.create_text_channel(
                f"ticket-{member.display_name}", category=category, overwrites=overwrites
            )
            await channel.send(f"Hello {member.mention}, thank you for opening the ticket, please explain your issue here.")


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def ticket(self, ctx, category: discord.CategoryChannel = None):
        if category is None:
            await ctx.send("Failed to configure the ticket system. Please provide a valid category.")
            return
        em = discord.Embed(title="**Coolest Ticket System Of All Time :)**", description="To create a ticket react with 🎫", color=0xEBD379)
        msg = await ctx.send(embed=em)
        await self.save_ticket_config(ctx.guild.id, msg.id, category.id)

        ticket_emoji = "\U0001F3AB"  # Unicode for 🎫
        await msg.add_reaction(ticket_emoji)
        await ctx.send("Successfully configured the ticket system.", delete_after=5.0)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def ticketdel(self, ctx):
        await self.close_connection()

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM ticket_configs WHERE guild_id = ?", (ctx.guild.id,))
            await db.commit()
        
        await ctx.send("Ticket system configuration has been deleted for this server.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def close(self, ctx):
        config = await self.get_ticket_config(ctx.guild.id)
        if config is None:
            return await ctx.send("Ticket system is not configured for this server.")

        category_id = int(config[1])
        category = discord.utils.get(ctx.guild.categories, id=category_id)

        if category is None:
            return await ctx.send("Ticket category not found.")

        if ctx.channel.category == category:
            if ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.administrator:
                await ctx.send("Ticket closed. The channel will be deleted in `15` seconds.")
                await asyncio.sleep(15)
                await ctx.channel.delete()
            else:
                await ctx.send("You don't have permission to close this ticket.")
        else:
            await ctx.send("You can only use the close command within the ticket category.")
        
async def setup(bot):
    await bot.add_cog(Ticket(bot))
