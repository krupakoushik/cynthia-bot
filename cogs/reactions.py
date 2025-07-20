import discord
import aiohttp

from aiohttp import ClientSession
from discord.ext import commands


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tableflip(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/tableflip.gif"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unflip(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/unflip.gif"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trigger(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/triggered.gif"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def delet(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/delet_this.png"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def weirdshit(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/weirdshit.jpg"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def filth(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/filth.gif"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def heckoff(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/heckoff.png"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def repost(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/repost.gif"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boi(self, ctx):
        await ctx.channel.typing()
        await ctx.reply(file=discord.File("assets/imgs/reactions/boi.jpg"))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/kiss')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/lick')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/hug')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def baka(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/baka')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cry(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/cry')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poke(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/poke')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smug(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/smug')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/slap')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tickle(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/tickle')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/pat')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def laugh(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/laugh')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feed(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/feed')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.nekos.fun:8080/api/cuddle')
            dogjson = await request.json()
        await ctx.reply(dogjson['image'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def wink(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/animu/wink')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def facepalm(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                'https://some-random-api.com/animu/face-palm')
            dogjson = await request.json()
            await ctx.reply(dogjson['link'])


async def setup(bot):
    await bot.add_cog(Reactions(bot))
