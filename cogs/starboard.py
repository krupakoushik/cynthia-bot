import discord
from discord.ext import commands
import aiosqlite
import os

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join("db", "starboard.db")
        self.db = None
        self.starboard_data = {}

    async def create_table(self):
        self.db = await aiosqlite.connect(self.db_path)
        cursor = await self.db.cursor()
        await cursor.execute("CREATE TABLE IF NOT EXISTS starboard_data (guild_id INTEGER PRIMARY KEY, channel_id INTEGER)")
        await self.db.commit()
        print("Table 'starboard_data' created successfully")

    async def close_connection(self):
        if self.db:
            await self.db.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()

    async def load_starboard_data(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM starboard_data") as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    self.starboard_data[str(row[0])] = {"channel_id": row[1]}

    async def save_starboard_data(self):
        async with aiosqlite.connect(self.db_path) as db:
            for guild_id, data in self.starboard_data.items():
                channel_id = data.get("channel_id", None)
                if channel_id:
                    await db.execute("INSERT OR REPLACE INTO starboard_data (guild_id, channel_id) VALUES (?, ?)", (guild_id, channel_id))
            await db.commit()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == "⭐":
            if reaction.count >= 3:
                guild_id = str(reaction.message.guild.id)
                if guild_id in self.starboard_data:
                    starboard_channel_id = self.starboard_data[guild_id].get("channel_id")
                    if starboard_channel_id:
                        starboard_channel = self.bot.get_channel(int(starboard_channel_id))
                        if starboard_channel:
                            starred_message = reaction.message

                            content = starred_message.content
                            author = starred_message.author.mention
                            jump_url = starred_message.jump_url

                            star_count = reaction.count
                            attachments = []
                            if starred_message.attachments:
                                attachments = [attachment.url for attachment in starred_message.attachments]

                            starboard_message_id = self.starboard_data[guild_id].get(starred_message.id)
                            if starboard_message_id:
                                try:
                                    starboard_message = await starboard_channel.fetch_message(starboard_message_id)
                                    starboard_embed = starboard_message.embeds[0]
                                    starboard_embed.set_author(
                                        name=f"⭐ {star_count} | {starred_message.channel.name} | ID: {starred_message.id}",
                                        icon_url=starred_message.author.avatar.url
                                    )
                                    await starboard_message.edit(embed=starboard_embed)
                                except discord.NotFound:
                                    del self.starboard_data[guild_id][starred_message.id]
                            else:
                                starboard_message = discord.Embed(color=0xEBD379)
                                starboard_message.set_author(
                                    name=f"⭐ {star_count} | {starred_message.channel.name} | ID: {starred_message.id}",
                                    icon_url=starred_message.author.avatar.url
                                )
                                starboard_message.description = f"By: {author}\n[Jump!]({jump_url})\n\n{content}"
                                if attachments:
                                    starboard_message.set_image(url=attachments[0])

                                starboard_message.set_footer(text="Starred Message", icon_url=self.bot.user.avatar.url)
                                starboard_message.timestamp = reaction.message.created_at

                                starboard_message = await starboard_channel.send(embed=starboard_message)
                                self.starboard_data[guild_id][starred_message.id] = starboard_message.id
                                self.save_starboard_data()

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def starboard(self, ctx, channel: discord.TextChannel = None):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.starboard_data:
            self.starboard_data[guild_id] = {}

        if channel is None:
            if guild_id in self.starboard_data and "channel_id" in self.starboard_data[guild_id]:
                starboard_channel_id = self.starboard_data[guild_id]["channel_id"]
                starboard_channel = self.bot.get_channel(int(starboard_channel_id))
                if starboard_channel:
                    embed = discord.Embed(
                        title="Starboard Channel of this server is:",
                        description=starboard_channel.mention,
                        color=0xEBD379
                    )
                else:
                    embed = discord.Embed(
                        title="Starboard Channel for this server is not set.",
                        color=0xEBD379
                    )
            else:
                embed = discord.Embed(
                    title="Starboard Channel for this server is not set.",
                    color=0xEBD379
                )
        else:
            self.starboard_data[guild_id]["channel_id"] = channel.id
            await self.save_starboard_data()
            embed = discord.Embed(
                title="Starboard Channel for this server is successfully set to:",
                description=channel.mention,
                color=0xEBD379
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Starboard(bot))
