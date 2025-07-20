import discord
from discord.ext import commands
import easy_pil
from easy_pil import Canvas, Editor, Font, load_image_async
from discord import File
import random
import aiosqlite
import os
import requests
from PIL import Image

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join("db", "welcomesys.db")
        self.db = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = await self.get_welcome_config(member.guild.id)
        if config is None:
            return

        channel_id, message, bg_imgur_link = config
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        if "{member}" in message:
            message = message.replace("{member}", member.mention)

        if bg_imgur_link:
            response = requests.get(bg_imgur_link)

            if response.status_code == 200:
                with open("bg_image.png", "wb") as f:
                    f.write(response.content)

                try:
                    pil_image = Image.open("bg_image.png")
                    print("Successfully opened the downloaded image!")
                except Exception as e:
                    print(f"Failed to open the downloaded image: {e}")
                    pil_image = None

                if pil_image:
                    background = Editor("bg_image.png").resize((800, 450))
                    os.remove("bg_image.png")
                else:
                    background = Editor("data/bg.jpg").resize((800, 450))
            else:
                background = Editor("data/bg.jpg").resize((800, 450))
        else:
            background = Editor("data/bg.jpg").resize((800, 450))


        profile_image = await load_image_async(str(member.avatar.url))
        profile = Editor(profile_image).resize((150, 150)).circle_image()

        poppins = Font.caveat(size=65)
        poppins_small = Font.caveat(size=50)
        poppins_light = Font.caveat(size=30)

        background.paste(profile, (325, 90))
        background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)
        background.text(
            (400, 260),
            f"Welcome to {member.guild.name}",
            color="white",
            font=poppins,
            align="center",
            stroke_width=int(2),
        )
        background.text(
            (400, 325),
            f"{member.display_name}",
            color="white",
            font=poppins_small,
            align="center",
            stroke_width=1,
        )
        background.text(
            (400, 380),
            f"Member {member.guild.member_count}",
            color="white",
            font=poppins_light,
            align="center",
            stroke_width=1,
        )

        file = discord.File(fp=background.image_bytes, filename="welcome.jpg")

        await channel.send(message, file=file)

    async def get_db_path(self):
        return os.path.join("db", "welcomesys.db")

    async def create_table(self):
        self.db = await aiosqlite.connect(self.db_path)
        cursor = await self.db.cursor()
        await cursor.execute(
            "CREATE TABLE IF NOT EXISTS welcome_configs (guild_id INTEGER PRIMARY KEY, channel_id INTEGER, message TEXT, bg_imgur_link TEXT)"
        )
        await self.db.commit()
        print("Table 'welcome' created successfully")

    async def close_connection(self):
        if self.db:
            await self.db.close()

    async def save_welcome_config(self, guild_id, channel_id, message, bg_imgur_link):
        db_path = await self.get_db_path()
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO welcome_configs (guild_id, channel_id, message, bg_imgur_link) VALUES (?, ?, ?, ?)",
                (guild_id, channel_id, message, bg_imgur_link if bg_imgur_link else ""),
            )
            await db.commit()

    async def get_welcome_config(self, guild_id):
        db_path = await self.get_db_path()
        async with aiosqlite.connect(db_path) as db:
            cursor = await db.execute(
                "SELECT channel_id, message, bg_imgur_link FROM welcome_configs WHERE guild_id = ?",
                (guild_id,),
            )
            return await cursor.fetchone()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()

    @commands.hybrid_command(with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx, channel: discord.TextChannel, message=None):
        if message is None:
            message = "Welcome to our server, have fun {member} :)"

        bg_imgur_link = None
        if ctx.message.attachments and ctx.message.attachments[0].url.endswith((".png", ".jpg", ".jpeg", ".gif")):
            bg_imgur_link = ctx.message.attachments[0].url

        await self.save_welcome_config(ctx.guild.id, channel.id, message, bg_imgur_link)
        await ctx.send(f"Welcome channel set to {channel.mention} with custom message. Make sure the background dimensions are `3840x2160`. You can mention the member by adding `{{member}}` tag in your message.\n```{message}```")

    @commands.hybrid_command(with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def welcomedel(self, ctx):
        await self.close_connection()

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM welcome_configs WHERE guild_id = ?", (ctx.guild.id,))
            await db.commit()
        
        await ctx.send("welcome system is deleted for this server.")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
