import discord
from discord.ext import commands
import aiohttp
from aiohttp import ClientSession

class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()
        
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    @commands.group()
    async def animals(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(title="List of Animal Pictures you can get:", description="- bird\n- cat\n- dog\n- duck\n- fox\n- kangaroo\n- koala\n- panda\n- pikachu\n- racoon\n- redpanda\n- whale", color=0xebd379)
            em.set_footer(text="example: ?animals cat")
            return await ctx.send(embed=em)

    @animals.command(name="dog", with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def dog(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.com/img/dog')
            factjson = await request2.json()
        await ctx.reply(factjson['link'])


    @animals.command(aliases=["neko"])
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def cat(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/cat')
            dogjson = await request.json()
            await ctx.reply(dogjson['link'])

    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def fox(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/fox')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])


    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def bird(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/bird')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])


    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/koala')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])

    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def redpanda(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/red_panda')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])


    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def racoon(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/raccoon')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])


    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def kangaroo(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/kangaroo')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])


    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def duck(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://random-d.uk/api/v2/random')
            dogjson = await request.json()
        await ctx.reply(dogjson['url'])


    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def whale(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/whale')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])

    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/panda')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])


    @animals.command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def pikachu(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/img/pikachu')
            dogjson = await request.json()
        await ctx.reply(dogjson['link'])


async def setup(bot):
    await bot.add_cog(Animals(bot))