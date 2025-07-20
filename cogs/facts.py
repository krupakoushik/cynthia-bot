import discord
import aiohttp
import random
from discord import File
from aiohttp import ClientSession
from discord.ext import commands

class Facts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()
        
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    @commands.group()
    async def afacts(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(title="List of Animal Facts you can get:", description="- bird\n- cat\n- dog\n- elephant\n- fox\n- giraffe\n- kangaroo\n- koala\n- panda\n- raccoon\n- whale", color=0xebd379)
            em.set_footer(text="example: ?afacts dog")
            await ctx.send(embed=em)

    @afacts.command()
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def dog(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.com/facts/dog')
            factjson = await request2.json()
        await ctx.reply(factjson['fact'])


    @afacts.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def cat(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.com/facts/cat')
            factjson = await request2.json()
        await ctx.reply(factjson['fact'])

        
    @afacts.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def fox(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.com/facts/fox')
            factjson = await request2.json()
        await ctx.reply(factjson['fact'])


    @afacts.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def kangaroo(self, ctx):
        async with aiohttp.ClientSession() as session:
                            request2 = await session.get('https://some-random-api.com/animal/kangaroo')
        factjson = await request2.json()
        await ctx.reply(factjson['fact'])


    @afacts.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def racoon(self, ctx):
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.com/animal/raccoon')
            factjson = await request2.json()
        await ctx.reply(factjson['fact'])


    @afacts.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.com/facts/koala')
            factjson = await request2.json()
        await ctx.reply(factjson['fact'])


    @afacts.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def bird(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.com/facts/bird')
            factjson = await request2.json()
        await ctx.reply(factjson['fact'])


    @afacts.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def panda(self, ctx):
        
        async with aiohttp.ClientSession() as session:
            request2 = await session.get('https://some-random-api.com/facts/panda')
            factjson = await request2.json()
        await ctx.reply(factjson['fact'])

    @commands.command(aliases = ['uselessfact'])
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def uf(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://uselessfacts.jsph.pl/api/v2/facts/random') as r:
                res = await r.json()

        await ctx.reply(res['text'])

    @commands.command(aliases=['number', 'numfact'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def numberfact(self, ctx, number: int):
        if not number:
            await ctx.reply(f'Usage: `{ctx.prefix}numberfact <number>`')
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'http://numbersapi.com/{number}?json') as resp:
                    file = await resp.json()
                    fact = file['text']
                    await ctx.reply(f"**Did you know?**\n*{fact}*")
        except KeyError:
            await ctx.reply("No facts are available for that number.")


    @commands.command(aliases=['year', 'yfact'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yearfact(self, ctx, number: int):
        if not number:
            await ctx.reply(f'Usage: `{ctx.prefix}numberfact <number>`')
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'http://numbersapi.com/{number}/year?json') as resp:
                    file = await resp.json()
                    fact = file['text']
                    await ctx.reply(f"**Did you know?**\n*{fact}*")
        except KeyError:
            await ctx.reply("No facts are available for that number.")


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://nekos.life/api/v2/fact')
            trump = await request.json()

            await ctx.reply(trump['fact'])


async def setup(bot):
    await bot.add_cog(Facts(bot)) 
