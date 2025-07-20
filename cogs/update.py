import discord
from discord.ext import commands

class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users_channel_id = 1132282407798706307
        self.bots_channel_id = 1132282410034266125
        self.total_channel_id = 1132282412118835270
        self.allowed_guild_id = 877565401813368843

    async def update_voice_channel_counts(self, guild):
        users_channel = guild.get_channel(self.users_channel_id)
        bots_channel = guild.get_channel(self.bots_channel_id)
        total_channel = guild.get_channel(self.total_channel_id)

        user_count = len([member for member in guild.members if not member.bot])
        bot_count = len([member for member in guild.members if member.bot])
        total_count = len(guild.members)

        await users_channel.edit(name=f'Users: {user_count}')
        await bots_channel.edit(name=f'Bots: {bot_count}')
        await total_channel.edit(name=f'Total: {total_count}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != self.allowed_guild_id:
            return
        await self.update_voice_channel_counts(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != self.allowed_guild_id:
            return
        await self.update_voice_channel_counts(member.guild)

async def setup(bot):
    await bot.add_cog(Update(bot))
