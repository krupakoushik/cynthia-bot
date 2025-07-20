import discord
import collections
import datetime
import time
import random
import asyncio
import ago

from ago import human
from random import choice, randint
from discord.ext import commands, tasks
from discord.ext.commands import clean_content
from discord.ext.tasks import loop

afk_list = []


def h(*, randomcolor=False):
    return random.randint(0, 255**3)


class Misc(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot
        self.data = []
        self.sniped_messages = {}

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.sniped_messages[message.guild.id] = {
            'content': message.content,
            'author': message.author,
            'channel_name': message.channel.name,
            'time': message.created_at,
            'event_type': 'deleted'
        }

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.sniped_messages[before.guild.id] = {
            'content': before.content,
            'author': before.author,
            'channel_name': before.channel.name,
            'time': before.created_at,
            'event_type': 'edited',
            'edited_content': after.content
        }

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def snipe(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.sniped_messages:
            await ctx.reply("Couldn't find a message to snipe!")
            return

        sniped_message = self.sniped_messages[guild_id]
        content = sniped_message['content']
        author = sniped_message['author']
        channel_name = sniped_message['channel_name']
        time = sniped_message['time']
        event_type = sniped_message['event_type']
        edited_content = sniped_message.get('edited_content')

        embed = discord.Embed(color=0xEBD379, timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar.url)
        embed.set_footer(text=f"{event_type.capitalize()} in #{channel_name}")

        if event_type == 'edited':
            embed.add_field(name="Original Message", value=content, inline=False)
            embed.add_field(name="Edited Message", value=edited_content, inline=False)
        else:
            embed.description = content

        await ctx.reply(embed=embed)



    @commands.hybrid_command(with_app_command=True)
    async def afk(self, ctx, *, args=None):
        if args is None:
            args = "AFK"
        self.data.append(ctx.author.id)
        self.data.append(args)
        await ctx.author.edit(nick=f'[AFK] {ctx.author.name}')
        await ctx.reply(f"{ctx.author.mention} has been set to AFK!")

    @commands.Cog.listener()
    async def on_message(self, message):
        for i in range(len(self.data)):
            if (f"<@{self.data[i]}>" in message.content) and (not message.author.bot):
                await message.reply(f"{message.author.mention}, You blind? Can't you see their nickname? <@{self.data[i]}> is away right now, they said: {self.data[i+1]}")
                return None
                break

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if user.id in self.data:
            i = self.data.index(user.id)
            self.data.remove(self.data[i+1])
            self.data.remove(user.id)
            nick = user.name.replace('[AFK]', '')
            await user.edit(nick=nick)
            await channel.send(f"{user.mention} is no longer afk!")

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def ping(self, ctx):
        latency = round(self.Bot.latency * 1000)
        await ctx.reply(f'{ctx.message.author.name}, Pong! ``{latency}``ms')

    @commands.command(aliases=['av'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, *, user: discord.Member = None):
        if not user:
            user = ctx.author

        await ctx.reply(user.avatar.url)

    @commands.command(aliases=['whois', 'ui'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        uroles = []
        for role in member.roles[1:]:
            if role.is_default():
                continue
            uroles.append(role.mention)
        uroles.reverse()

        time = member.created_at
        time1 = member.joined_at
        timestamp = 'ㅤ'
        if member.status == discord.Status.online:
            status = '🟢'
        elif member.status == discord.Status.idle:
            status = '🌙'
        elif member.status == discord.Status.dnd:
            status = '⛔'
        elif member.status == discord.Status.offline:
            status = '⚪'
        if member.activity is None:
            activity = 'None'
        else:
            activity = member.activities[-1].name
            try:
                timestamp = member.activities[0].details
            except:
                timestamp = 'ㅤ'

        embed = discord.Embed(
            color=0xEBD379, timestamp=ctx.message.created_at, type="rich")
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="__General information__", value=f'**Nickname :** {member.display_name}\n'
                        f'**ID :** {member.id}\n'
                        f'**Account created :** {human(time, 4)}\n'
                        f'**Server joined :** {human(time1, 3)}\n', inline=False)
        embed.add_field(name="__Role info__", value=f'**Highest role :** {member.top_role.mention}\n'
                        f'**Color** : {member.color}\n'
                        f'**Role(s) :** {", ".join(uroles)}\n', inline=False)
        embed.add_field(name="__Presence__", value=f'**Status : ** {status}\n'
                        f'**Activity : ** {activity}\nㅤㅤㅤㅤ{timestamp}')
        await ctx.reply(embed=embed)

    @commands.command(aliases=['servercount', 'membercount'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def members(self, ctx):
        embed = discord.Embed(color=0xEBD379)
        embed.add_field(name="Total members",
                        value=f"{ctx.guild.member_count}", inline=False)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['si'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx):
        guild = ctx.guild
        emojis = str(len(guild.emojis))

        channels = str(len(guild.channels))
        roles = str(len(guild.roles))
        time = ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p ")
        voice = str(len(guild.voice_channels))
        text = str(len(guild.text_channels))
        statuses = collections.Counter(
            [member.status for member in guild.members])

        online = statuses[discord.Status.online]
        idel = statuses[discord.Status.idle]
        dnd = statuses[discord.Status.dnd]
        offline = statuses[discord.Status.offline]

        embed = discord.Embed(timestamp=ctx.message.created_at, color=0xEBD379)

        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_author(name=f"Information for  {ctx.guild.name}")
        embed.add_field(name="__General information__\n", value=f'**Server name : ** {guild.name}\n'
                        f'**Server ID : ** {guild.id}\n'
                        f'**Created at : ** {time}\n'
                        f'**Verification level : ** {guild.verification_level} \n'
                        f'**Server owner : ** {guild.owner} \n', inline=False)

        embed.add_field(name="\n\n\n__Statistics__", value=f'**Member count : ** {ctx.guild.member_count}\n'
                        f'**Role count : ** {roles} \n'
                        f'**Channel count : ** {channels}\n'
                        f'**Text channels :** {text}\n'
                        f'**Voice channels :** {voice}\n'
                        f'**Emoji count : ** {emojis}\n'
                        f'**Server boosts : ** {guild.premium_subscription_count}\n')

        embed.add_field(name="__Activity__", value=f'🟢 {online}\n\n'
                        f'🌙 {idel}\n\n'
                        f'⛔ {dnd}\n\n'
                        f'⚪ {offline}\n\n')

        await ctx.reply(embed=embed)

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pingadv(self, ctx):
        msg = await ctx.reply("Pinging bot\'s latency...")
        times = []
        counter = 0
        embed = discord.Embed(title="More information:",
                              description="Pinged 3 times and calculated the average.", color=0xEBD379)

        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Pinging... {counter}/3")
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            embed.add_field(name=f"Ping {counter}:",
                            value=f"{speed}ms", inline=True)

        embed.set_author(name="Pong!", icon_url=ctx.author.avatar.url)
        embed.add_field(
            name="Bot latency", value=f"{round(self.Bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Average speed",
                        value=f"{round((round(sum(times)) + round(self.Bot.latency * 1000))/4)}ms")
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(
            text=f"Estimated total time elapsed: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: {round((round(sum(times)) + round(self.Bot.latency * 1000))/4)}ms", embed=embed)

    @commands.command(aliases=['cstats'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def channelstats(self, ctx):
        channel = ctx.channel
        tmembers = str(len(channel.members))
        nsfw = (ctx.channel.is_nsfw())
        news = (ctx.channel.is_news())
        embed = discord.Embed(color=0xEBD379, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(name="__Information__", value=f'**Server name: ** {ctx.guild.name} \n'
                        f'**Channel name :** {channel.name}\n'
                        f'**Channel ID : ** {channel.id} \n'
                        f'**Channel type : **{channel.type}\n'
                        f'**Channel category : ** {channel.category}\n'
                        f'**Topic : ** {channel.topic}\n'
                        f'**Channel position :** {channel.position}\n'
                        f'**Created at :** {channel.created_at.strftime("%a, %#d %B %Y, %I:%M %p ")}\n'
                        f'**Slowmode :** {channel.slowmode_delay}\n'
                        f'**Channel Permissions :** {channel.permissions_synced}\n'
                        f'**Channel members :** {tmembers}\n'
                        f'**Is nsfw : ** {nsfw}\n'
                        f'**Is news : ** {news}', inline=False)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def mods(self, ctx):
        message = ""
        all_status = {
            "online": {
                "users": [],
                "emoji": "🟢"
            },
            "idle": {
                "users": [],
                "emoji": "🟡"
            },
            "dnd": {
                "users": [],
                "emoji": "🔴"
            },
            "offline": {
                "users": [],
                "emoji": "⚪"
            }
        }

        for user in ctx.guild.members:
            user_perm = ctx.channel.permissions_for(user)
            if user_perm.kick_members or user_perm.ban_members:
                if not user.bot:
                    all_status[str(user.status)]["users"].append(f"**{user}**")

        for g in all_status:
            if all_status[g]["users"]:
                message += f"{all_status[g]['emoji']} {', '.join(all_status[g]['users'])}\n"

        await ctx.reply(f"Mods in **{ctx.guild.name}**\n{message}")


async def setup(Bot):
    await Bot.add_cog(Misc(Bot))
