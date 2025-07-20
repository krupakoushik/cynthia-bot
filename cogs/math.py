import discord
import asyncio
import os
import akinator
import sys
import math
import random

from discord.ext import commands
from random import shuffle


def add(n: float, n2: float):
    return n + n2


def sub(n: float, n2: float):
    return n - n2


def rando(n: int, n2: int):
    return random.randint(n, n2)


def div(n: float, n2: float):
    return n / n2


def sqrt(n: float):
    return math.sqrt(n)


def mult(n: float, n2: float):
    return n * n2


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    @commands.command()
    async def mathadd(self, ctx, x: float, y: float):
        try:
            result = add(x, y)
            await ctx.send(result)

        except:
            pass

    @commands.command()
    async def mathsub(self, ctx, x: float, y: float):
        try:
            result = sub(x, y)
            await ctx.send(result)

        except:
            pass

    @commands.command()
    async def mathrando(self, ctx, x: int, y: int):
        try:
            result = rando(x, y)
            await ctx.send(result)

        except:
            pass

    @commands.command()
    async def mathdiv(self, ctx, x: float, y: float):
        try:
            result = div(x, y)
            await ctx.send(result)

        except:
            pass

    @commands.command()
    async def mathmult(self, ctx, x: float, y: float):
        try:
            result = mult(x, y)
            await ctx.send(result)

        except:
            pass

    @commands.command()
    async def mathsqrt(self, ctx, x: float):
        try:
            result = sqrt(x)
            await ctx.send(result)

        except:
            pass


async def setup(bot):
    await bot.add_cog(Math(bot))
