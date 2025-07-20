import discord
import json
import os
import random

from datetime import datetime
from random import randint
from discord.ext import commands
from discord.ext.commands import clean_content, has_permissions, MissingPermissions


def h(*, randomcolor=False):
    return random.randint(0, 255**3)


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role < member.top_role:
            return await ctx.send("You can't kick someone higher than you.")
        if ctx.me.top_role < member.top_role:
            return await ctx.send("You can't kick a supreme being can you?")
        else:
            await member.kick(reason=reason)
            await ctx.send(f'User {member.mention} was kicked from the server for ``{reason}.``', delete_after=5.0)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = "You were banned from the server for not following the rules."):
        with open('assets/imgs/b1nzy_with_banhammer.png', 'rb') as f:
            picture = discord.File(f)
        if ctx.author.top_role < member.top_role:
            return await ctx.send("You can't ban someone higher than you.")
        if ctx.me.top_role < member.top_role:
            return await ctx.send("You can't ban a supreme being can you?")
        else:
            await member.send(file=picture)
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f'{member.mention} was banned from the server.')


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()

        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"Unbanned: {user.mention}", delete_after=5.0)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self ,ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if role not in guild.roles:
            perms = discord.Permissions(send_messages=False, speak=False)
            await guild.create_role(name="Muted", permissions=perms)
            await member.add_roles(role)
            await ctx.send(f"{member} was muted.")
        else:
            await member.add_roles(role)
            await ctx.send(f"{member} was muted.")

            
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name= "Muted")
        await member.remove_roles(role)
        await ctx.send(f"{member} was unmuted.")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user:discord.Member, *, reason:str):
        if user.id == self.bot.user.id:
            await ctx.send("Oh, REALLY now, huh? I do my best at maintaining this server and THIS is how you treat me? Screw this..")
            return
        if user.bot == 1:
            await ctx.send("It's useless to warn a bot. Why would you even try.")
            return
        if user == ctx.author:
            await ctx.send("Why the heck would you warn yourself? You hate yourself THAT much?")
            return
        if user.guild_permissions.manage_messages == True:
            await ctx.send("The specified user has the \"Manage Messages\" permission (or higher) inside the guild/server.")
            return
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if not os.path.exists("data/warns/" + str(ctx.guild.id) + "/"):
            os.makedirs("data/warns/" + str(ctx.guild.id) + "/")
        try:
            with open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json", "w") as f:
                data = ({
                    'offender_name':user.name,
                    'warns':1,
                    1:({
                        'mod_id':ctx.author.id,
                        'mod':ctx.author.name,
                        'reason':reason,
                        'channel':str(ctx.channel.id),
                        'datetime':dt_string
                    })
                })
                json.dump(data, f)
            embed = discord.Embed(title=f"{user.name}'s new warn",color=0xEBD379)
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar.url, url=f"https://discord.com/users/{ctx.message.author.id}/")
            embed.add_field(name="Warn 1", value=f"**Mod**: {ctx.author.name} (<@{ctx.author.id}>)\n**Reason**: {reason}\n**Channel**: <#{str(ctx.channel.id)}>\n**Date and Time**: {dt_string}",inline=True)
            await ctx.send(content="Successfully added new warn.", embed=embed)
          
            return
          
        warn_amount = data.get("warns")
        new_warn_amount = warn_amount + 1
        data["warns"]=new_warn_amount
        data["offender_name"]=user.name
        new_warn = ({
            'mod_id':ctx.author.id,
            'mod':ctx.author.name,
            'reason':reason,
            'channel':str(ctx.channel.id),
            'datetime':dt_string
        })
        data[new_warn_amount]=new_warn
        json.dump(data, open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json", "a"))

        embed = discord.Embed(
            title=f"{user.name}'s new warn",
            color=0xEBD379
        )
        embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar.url,url=f"https://discord.com/users/{ctx.message.author.id}/")
        embed.add_field(name=f"**Warn** {new_warn_amount}",value=f"**Mod**: {ctx.author.name} (<@{ctx.author.id}>)\n**Reason**: {reason}\n**Channel**: <#{str(ctx.channel.id)}>\n**Date and Time**: {dt_string}",inline=True)
        await ctx.send(content="Successfully added new warn.",embed=embed)
    

    @commands.command()
    async def warnings(self, ctx, user: discord.Member):
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await ctx.send(f"{ctx.author.name}, user [{user.name} ({user.id})] does not have any warns.")
            return

        warn_amount = data.get("warns")
        last_noted_name = data.get("offender_name")

        try:
            username = user.name
        except:
            username = last_noted_name

        warns_word = "warns" if warn_amount > 1 else "warn"  # Determine the plural form

        embed = discord.Embed(
            title=f"{username}'s warns",
            description=f"**They have {warn_amount} {warns_word}.**",
            color=0xEBD379
        )
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar.url,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )
        for x in range(1, warn_amount + 1):
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)

            warn_dict = data.get(str(x))
            warner_id = warn_dict.get('mod_id')
            try:
                warner_name = self.bot.get_user(id=warner_id)
            except:
                warner_name = warn_dict.get('mod')

            warn_reason = warn_dict.get('reason')
            warn_channel = warn_dict.get('channel')
            warn_datetime = warn_dict.get('datetime')

            embed.add_field(
                name=f"Warn {x}",
                value=f"**Mod**: {warner_name} (<@{warner_id}>)\n**Reason**: {warn_reason}\n**Channel**: <#{warn_channel}>\n**Date and Time**: {warn_datetime}",
                inline=True
            )
        await ctx.send(content=None, embed=embed)


    @commands.command(aliases=['removewarn','clearwarn', 'unwarn'])
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, user:discord.Member, *, warn:str):
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await ctx.send(f"{ctx.author.mention}, user {user.mention} does not have any warns.")
            return
        warn_amount = data.get('warns')
        specified_warn = data.get(warn)
        warn_warner = specified_warn.get('mod_id')
        warn_reason = specified_warn.get('reason')
        warn_channel = specified_warn.get('channel')
        warn_datetime = specified_warn.get('datetime')
        try:
            warn_warner_name = self.bot.get_user(id=warn_warner)
        except:
            warn_warner_name = specified_warn.get('mod')

        confirmation_embed = discord.Embed(title=f'**{user.name}\'s warn number {warn}**', description=f'**Mod**: {warn_warner_name}\n**Reason**: {warn_reason}\n**Channel**: <#{warn_channel}>\n**Date and Time**: {warn_datetime}',color=0xEBD379)
        confirmation_embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar.url, url=f"https://discord.com/users/{ctx.message.author.id}/")
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send(content='Are you sure you want to remove this warn? (Reply with y or n)', embed=confirmation_embed)
        msg = await self.bot.wait_for('message', check=check)
        reply = msg.content.lower()
        if reply in ('y', 'yes', 'confirm'):
            if warn_amount == 1:
                os.remove("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json")
                await ctx.send(f"{ctx.author.mention}, user {user.mention} has gotten their warn removed.")
                return
            if warn != warn_amount:
                for x in range(int(warn),int(warn_amount)):
                    data[str(x)] = data[str(x+1)]
                    del data[str(x+1)]
            else:
                del data[warn]
            data['warns']=warn_amount - 1
            json.dump(data,open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "w"))
            await ctx.send(f"[{ctx.author.name}], user [{user.name} ({user.id})] has gotten their warn removed.")
            return
        elif reply in ('n', 'no', 'cancel'):
            await ctx.send("Alright, action cancelled.")
            return
        else:
            await ctx.send("I have no idea what you want me to do. Action cancelled.")
    

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def editwarn(self, ctx, user:discord.Member, *, warn:str):
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await ctx.send(f"{ctx.author.mention}, user {user.mention} does not have any warns.")
            return


        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send(content='What would you like to change the warn\'s reason to?')
        msg = await self.bot.wait_for('message', check=check)
        warn_new_reason = msg.content.lower()

        specified_warn = data.get(warn)
        warn_warner = specified_warn.get('mod_id')
        warn_channel = specified_warn.get('channel')
        warn_datetime = specified_warn.get('datetime')
        try:
            warn_warner_name = self.bot.get_user(id=warn_warner)
        except:
            warn_warner_name = specified_warn.get('mod')

        confirmation_embed = discord.Embed(title=f'{user.name}\'s warn number {warn}',description=f'**Mod**: {warn_warner_name}\n**Reason**: {warn_new_reason}\n**Channel**: <#{warn_channel}>\n**Date and Time**: {warn_datetime}',color=0xEBD379)
        confirmation_embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar.url,url=f"https://discord.com/users/{ctx.message.author.id}/")

        await ctx.send(content='Are you sure you want to edit this warn like this? (Reply with y/yes or n/no)', embed=confirmation_embed)

        msg = await self.bot.wait_for('message', check=check)
        reply = msg.content.lower()
        if reply in ('y', 'yes', 'confirm'):
            specified_warn['reason']=warn_new_reason
            json.dump(data,open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "w"))
            await ctx.send(f"{ctx.author.mention}, user {user.mention} has gotten their warn edited.")
            return
        elif reply in ('n', 'no', 'cancel', 'flanksteak'):
            await ctx.send("Alright, action cancelled.")
            return
        else:
            await ctx.send("I have no idea what you want me to do. Action cancelled.")


    @commands.command(aliases=["clean"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=2):
        if amount <= 200:
            amt = await ctx.channel.purge(limit=(amount + 1))
            await ctx.send(f"**Cleared `{len(amt) - 1}` from this channel**", delete_after=5.0)
        else:
            await ctx.send("**Please provide a smaller number than 200**", delete_after=5.0)


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def slowmode(self, ctx, time):
        if time == 'remove':
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send(f'Slowmode removed.')
        else:
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.send(f'{time}s of slowmode was set on the current channel.')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name=f'Verified')
        await ctx.channel.set_permissions(role, send_messages=False, read_messages=True)
        await ctx.send("Channel locked.")


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx):
        hm = discord.utils.get(ctx.guild.roles, name=f'Verified')
        await ctx.channel.set_permissions(hm, send_messages=True, read_messages=True)
        await ctx.send("Channel unlocked.")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, *, arg):
        if ctx.guild.me.top_role < member.top_role:
            return await ctx.send("Admin :(")
        if ctx.message.author.top_role < member.top_role:
            return await ctx.send("You  have lower roles.")
        role = discord.utils.get(ctx.guild.roles, name=f"{arg}")

        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send(f"{member} was given role ``{arg}``.")
        else:
            await member.remove_roles(role)
            await ctx.send(f"{member} was removed from the role ``{arg}``.")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, id:int):
        message = await ctx.channel.fetch_message(id)
        await message.pin()
        await ctx.send("Successfully pinned the message.") 


    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def cnick(self, ctx, member: discord.Member, *, arg):
        if ctx.guild.me.top_role < member.top_role:
            return await ctx.send("Admin :(")
        if ctx.message.author.top_role < member.top_role:
            return await ctx.send("You  have lower roles.")
        else:
            await member.edit(nick=arg)
            await ctx.send(f'{member} nickname was changed to {arg} by {ctx.message.author}', delete_after=5.0)


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, question, *options):
        if len(options) <= 1:
            await ctx.send('Weird you want to make a poll with less than 1 option?')
            return
        if len(options) > 7:
            await ctx.send('Bruh! you can\'t make a poll with more than 7 options.')
            return

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']

        description = []
        for x, option in enumerate(options):
            description.append(f'\n\n {reactions[x]} {option}')
        embed = discord.Embed(title=question, description=''.join(description), color=0xEBD379, timestamp=ctx.message.created_at)
        embed.set_footer(text=f'Supreme being responsible for the poll: {ctx.message.author.name}')
        msg = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await msg.add_reaction(reaction)

        await msg.edit(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def userpurge(self, ctx, *, member: discord.Member):
      channel = ctx.message.channel
      member = member

      def check(msg):
        return msg.author.id == member.id

      await ctx.message.delete()
      await channel.purge(limit=None, check=check,)
      await ctx.send(f'All from {member.mention} have been purged by {ctx.author.mention}.', delete_after=5.0)


async def setup(bot):
    await bot.add_cog(Mod(bot))
