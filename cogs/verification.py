import discord
from discord.ext import commands

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_guild_id = 877565401813368843

    @commands.hybrid_command(with_app_command=True)
    async def verify(self, ctx):
        if ctx.guild.id != self.allowed_guild_id:
            return
        await ctx.channel.purge(limit=1)
        em = discord.Embed(description="**Nobody is gonna read this crap and just gonna react for access but if the mods/admins see your behavior to be bad, then suitable action will be taken :)**", color=0xEBD379)
        message = await ctx.send(embed=em)
        await message.add_reaction("<:gigachad:1127944751342166097>")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild.id != self.allowed_guild_id:
            return
        
        if payload.emoji.id == 1127944751342166097:
            if payload.channel_id == 1121779928870965278:
                member = guild.get_member(payload.user_id)
                role_id = 1127933704665305110
                role = guild.get_role(role_id)
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild.id != self.allowed_guild_id:
            return
        
        if payload.emoji.id == 1127944751342166097:
            if payload.channel_id == 1121779928870965278:
                member = guild.get_member(payload.user_id)
                role_id = 1127933704665305110
                role = guild.get_role(role_id)
                await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(Verify(bot))
