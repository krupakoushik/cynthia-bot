import discord
from discord.ext import commands
import aiosqlite
import random
import easy_pil
from easy_pil import Canvas, Editor, Font, load_image_async
from discord import File
import os
import asyncio

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join("db", "level.db")
        self.db = None

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    async def create_table(self):
        self.db = await aiosqlite.connect(self.db_path)
        cursor = await self.db.cursor()
        await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER);")
        await cursor.execute("CREATE TABLE IF NOT EXISTS levelSettings (levelsys BOOL, role INTEGER, levelreq INTEGER, channel INTEGER, guild INTEGER);")
        await self.db.commit()
        print("Tables 'levels' and 'levelSettings' created successfully")

    async def close_connection(self):
        if self.db:
            await self.db.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_table()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild = message.guild
        if not guild:
            return

        async with self.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys, channel FROM levelSettings WHERE guild = ?", (guild.id,))
            level_settings = await cursor.fetchone()
            if not level_settings or not level_settings[0]:
                return

            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (message.author.id, guild.id))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (message.author.id, guild.id))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, message.author.id, guild.id))
            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

            if level < 5:
                xp += random.randint(1, 3)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, message.author.id, guild.id))
            else:
                rand = random.randint(1, level // 4)
                if rand == 1:
                    xp += random.randint(1, 3)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, message.author.id, guild.id))

            while xp >= (level + 1) * 100:
                level += 1
                await cursor.execute("SELECT role FROM levelSettings WHERE levelreq = ? AND guild = ?", (level, guild.id))
                role = await cursor.fetchone()
                await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, message.author.id, guild.id))
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, message.author.id, guild.id))

                if role:
                    role = role[0]
                    role = guild.get_role(role)
                    try:
                        await message.author.add_roles(role)
                        if level_settings[1]:
                            levelup_channel = self.bot.get_channel(level_settings[1])
                            if levelup_channel:
                                await levelup_channel.send(f"{message.author.mention}, You have leveled up to level **{level}** and received **{role.name}** role!")
                        else:
                            await message.channel.send(f"{message.author.mention}, You have leveled up to level **{level}** and received **{role.name}** role!")
                    except discord.HTTPException:
                        if level_settings[1]:
                            levelup_channel = self.bot.get_channel(level_settings[1])
                            if levelup_channel:
                                await levelup_channel.send(f"{message.author.mention}, You have leveled up to level **{level}**!")
                        else:
                            await message.channel.send(f"{message.author.mention}, You have leveled up to level **{level}**!")
                else:
                    if level_settings[1]:
                        levelup_channel = self.bot.get_channel(level_settings[1])
                        if levelup_channel:
                            await levelup_channel.send(f"{message.author.mention}, You have leveled up to level **{level}**!")
                    else:
                        await message.channel.send(f"{message.author.mention}, You have leveled up to level **{level}**!")

        await self.db.commit()


    @commands.hybrid_command(aliases=["lvl"], with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        async with self.db.cursor() as cursor:
            await cursor.execute(
                "SELECT levelsys FROM levelSettings WHERE guild = ?",
                (ctx.guild.id,)
            )
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                return

            await cursor.execute(
                "SELECT xp, level, (SELECT COUNT(*) FROM levels WHERE level > l.level OR (level = l.level AND xp > l.xp) AND guild = ?) + 1 AS rank FROM levels l WHERE user = ? AND guild = ?",
                (ctx.guild.id, member.id, ctx.guild.id),
            )
            result = await cursor.fetchone()

            if not result:
                await ctx.send("Member not found.")
                return

            xp, level, rank = result

            user_data = {
                "xp": xp,
                "level": level,
                "next_level_xp": (level + 1) * 100,
                "rank": rank,
            }

            background = Editor(Canvas((934, 282), color="#2C2F33"))
            profile_image = await load_image_async(str(member.avatar.url))
            profile = Editor(profile_image).resize((150, 150)).circle_image()

            card_right_shape = [(650, 0), (750, 300), (934, 300), (934, 0)]

            background.polygon(card_right_shape, "#EBD379")

            belanosima = Font.montserrat(size=40)
            belanosima_small = Font.montserrat(size=30)

            background.paste(profile, (30, 30))

            percentage = (user_data["xp"] / user_data["next_level_xp"]) * 100

            background.rectangle(
                (30, 220), width=650, height=40, fill="#EDEAE0", radius=15
            )
            background.bar(
                (30, 220),
                max_width=650,
                height=40,
                percentage=percentage,
                fill="#EBD379",
                radius=15,
            )
            background.text(
                (200, 40),
                member.display_name,
                font=belanosima,
                color="white",
                stroke_width=1,
            )

            background.rectangle((200, 100), width=350, height=2, fill="#EBD379")

            background.text(
                (200, 130),
                f"Level : {user_data['level']} | XP : {user_data['xp']} / {user_data['next_level_xp']} | Rank : {user_data['rank']}",
                font=belanosima_small,
                color="white",
                stroke_width=1,
            )

            card = File(fp=background.image_bytes, filename="rank.png")
            await ctx.send(file=card)

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lb(self, ctx, page: int = 1):
        if page < 1:
            return await ctx.send("Invalid page number. The page number must be greater than or equal to 1.")

        async with self.db.cursor() as cursor:
            await cursor.execute(
                "SELECT levelsys FROM levelSettings WHERE guild = ?",
                (ctx.guild.id,)
            )
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                return

            await cursor.execute(
                "SELECT user, xp, level FROM levels WHERE guild = ? ORDER BY level DESC, xp DESC",
                (ctx.guild.id,),
            )
            results = await cursor.fetchall()

            if not results:
                return await ctx.send("No users found.")

            max_lines = 10
            total_pages = (len(results) + max_lines - 1) // max_lines

            if page > total_pages:
                return await ctx.send(f"Page {page} does not exist.")

            start_index = (page - 1) * max_lines
            end_index = start_index + max_lines
            page_results = results[start_index:end_index]

            leaderboard = f"{ctx.guild.name} Leaderboard (Page {page}/{total_pages}):\n\n"

            for index, row in enumerate(page_results, start=start_index + 1):
                member_id, xp, level = row
                member = ctx.guild.get_member(member_id)
                if member:
                    leaderboard += f"{index}. {member.display_name} - Level {level} (XP: {xp})\n"

            leaderboard_color = "#EBD379"
            leaderboard_text_color = "#2C2F33"

            background = Editor(Canvas((500, 500), color=leaderboard_color))

            leaderboard_font = Font.poppins(size=22)

            lines = leaderboard.splitlines()
            line_height = 25

            y = 50
            for line in lines:
                background.text(
                    (50, y),
                    line,
                    font=leaderboard_font,
                    color=leaderboard_text_color,
                )
                y += line_height

            leaderboard_file = File(fp=background.image_bytes, filename="leaderboard.png")

            leaderboard_message = None
            async for message in ctx.channel.history(limit=10):
                if message.id == ctx.message.id:
                    continue
                if message.author.id == self.bot.user.id and message.embeds and message.embeds[0].title == f"{ctx.guild.name} Leaderboard (Page {page}/{total_pages}):":
                    leaderboard_message = message
                    break

            if leaderboard_message:
                await leaderboard_message.edit(file=leaderboard_file)
            else:
                leaderboard_message = await ctx.send(file=leaderboard_file)

            if total_pages > 1:
                await leaderboard_message.add_reaction("⬅️")
                await leaderboard_message.add_reaction("➡️")

            def reaction_check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == leaderboard_message.id

            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=reaction_check)
            except asyncio.TimeoutError:
                return

            if str(reaction.emoji) == "⬅️" and page > 1:
                await self.lb(ctx, page - 1)
            elif str(reaction.emoji) == "➡️" and page < total_pages:
                await self.lb(ctx, page + 1)

            try:
                await leaderboard_message.clear_reactions()
            except discord.HTTPException:
                pass


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rewards(self, ctx):
        async with self.db.cursor() as cursor:
            await cursor.execute(
                "SELECT levelsys FROM levelSettings WHERE guild = ?",
                (ctx.guild.id,)
            )
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                return

            await cursor.execute(
                "SELECT levelreq, role FROM levelSettings WHERE guild = ?",
                (ctx.guild.id,)
            )
            rolelvls = await cursor.fetchall()
            
        if not rolelvls:
            return await ctx.send("No level reward roles have been set up for this server!")

        em = discord.Embed(title="Role Rewards", description="", color=0xEBD379)

        for level, role_id in rolelvls:
            role = ctx.guild.get_role(role_id)
            if role is not None:
                em.description += f"Level **{level}**: {role.mention}\n"

        await ctx.send(embed=em)

    @commands.hybrid_command(with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def setrole(self, ctx, level: int, *, role: discord.Role):
            async with self.db.cursor() as cursor:
                await cursor.execute(
                    "SELECT levelsys FROM levelSettings WHERE guild = ?",
                    (ctx.guild.id,)
                )
                levelsys = await cursor.fetchone()
                if levelsys and not levelsys[0]:
                    return

                await cursor.execute(
                    "SELECT role FROM levelSettings WHERE role = ? AND guild = ?",
                    (role.id, ctx.guild.id)
                )
                roleTF = await cursor.fetchone()

                await cursor.execute(
                    "SELECT role FROM levelSettings WHERE levelreq = ? AND guild = ?",
                    (level, ctx.guild.id)
                )
                levelTF = await cursor.fetchone()

                if roleTF or levelTF:
                    return await ctx.send("A role or level setting for that value already exists!")

                await cursor.execute(
                    "INSERT INTO levelSettings VALUES (?, ?, ?, ?, ?)",
                    (True, role.id, level, 0, ctx.guild.id)
                )
                await self.db.commit()
                await ctx.send("Added that level role :)")

    @commands.hybrid_command(with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def removerole(self, ctx, role: discord.Role):
        async with self.db.cursor() as cursor:
            await cursor.execute(
                "SELECT levelsys FROM levelSettings WHERE guild = ?",
                (ctx.guild.id,)
            )
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                return

            await cursor.execute(
                "SELECT role FROM levelSettings WHERE role = ? AND guild = ?",
                (role.id, ctx.guild.id)
            )
            roleTF = await cursor.fetchone()

            await cursor.execute(
                "SELECT role FROM levelSettings WHERE levelreq = ? AND guild = ?",
                (role.id, ctx.guild.id)
            )
            levelTF = await cursor.fetchone()

            if not roleTF and not levelTF:
                return await ctx.send("No role or level setting found for that value!")

            if roleTF:
                await cursor.execute(
                    "DELETE FROM levelSettings WHERE role = ? AND guild = ?",
                    (role.id, ctx.guild.id)
                )
            elif levelTF:
                await cursor.execute(
                    "DELETE FROM levelSettings WHERE levelreq = ? AND guild = ?",
                    (role.id, ctx.guild.id)
                )

            await self.db.commit()

        await ctx.send("Removed that level role or level setting.")

    @commands.hybrid_command(with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def levele(self, ctx, levelup_channel: discord.TextChannel = None):
        async with self.db.cursor() as cursor:
            await cursor.execute(
                "SELECT levelsys FROM levelSettings WHERE guild = ?",
                (ctx.guild.id,)
            )
            levelsys = await cursor.fetchone()
            if levelsys:
                if levelsys[0]:
                    return await ctx.send("Level system is already enabled for this server!")
                await cursor.execute(
                    "UPDATE levelSettings SET levelsys = ? WHERE guild = ?",
                    (True, ctx.guild.id,)
                )
            else:
                await cursor.execute(
                    "INSERT INTO levelSettings (levelsys, role, levelreq, channel, guild) VALUES (?, ?, ?, ?, ?)",
                    (True, 0, 0, 0, ctx.guild.id,)
                )
            
            if levelup_channel:
                await cursor.execute(
                    "UPDATE levelSettings SET channel = ? WHERE guild = ?",
                    (levelup_channel.id, ctx.guild.id)
                )
            else:
                await cursor.execute(
                    "UPDATE levelSettings SET channel = ? WHERE guild = ?",
                    (ctx.channel.id, ctx.guild.id)
                )
            
            await ctx.send("Successfully enabled the **COOLEST LEVELING SYSTEM** :)")
            await self.db.commit()


    @commands.hybrid_command(with_app_command=True)
    @commands.has_permissions(manage_guild=True)
    async def leveld(self, ctx):
        async with self.db.cursor() as cursor:
            await cursor.execute(
                "SELECT levelsys FROM levelSettings WHERE guild = ?",
                (ctx.guild.id,)
            )
            levelsys = await cursor.fetchone()
            if levelsys:
                if not levelsys[0]:
                    return await ctx.send("Level system is already disabled for this server!")
                await cursor.execute(
                    "UPDATE levelSettings SET levelsys = ? WHERE guild = ?",
                    (False, ctx.guild.id,)
                )
            else:
                await cursor.execute(
                    "INSERT INTO levelSettings VALUES (?, ?, ?, ?, ?)",
                    (False, 0, 0, 0, ctx.guild.id,)
                )
            await ctx.send("Successfully disabled the **COOLEST LEVELING SYSTEM** :)")

        await self.db.commit()

async def setup(bot):
    await bot.add_cog(Level(bot))
