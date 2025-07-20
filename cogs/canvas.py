import discord
import aiohttp
import io

from aiohttp import ClientSession
from discord.ext import commands


class Canvas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()
        
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def triggered(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://some-random-api.com/canvas/overlay/triggered?avatar={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'triggered.gif'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def comrade(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://some-random-api.com/canvas/overlay/comrade?avatar={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'comrade.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://some-random-api.com/canvas/overlay/gay?avatar={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'gay.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glass(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://some-random-api.com/canvas/overlay/glass?avatar={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'glass.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wasted(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://some-random-api.com/canvas/overlay/wasted?avatar={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'wasted.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def passed(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://some-random-api.com/canvas/overlay/passed?avatar={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'passed.jpeg'))



    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def horny(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.com/canvas/horny?avatar={member.avatar.url}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply('No horny :(')
                await session.close()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def simp(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.com/canvas/simpcard?avatar={member.avatar.url}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "simp.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply('No card for you :(')
                await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pet(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://api.popcat.xyz/pet?image={member.avatar.url}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "pet.gif")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply('No card for you :(')
                await session.close()



    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jail(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/jail?image={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'jail.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gun(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/gun?image={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'gun.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def threat(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        rofl = member.avatar.url
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=threats&url={rofl}')
            dogjson = await request.json() 
            await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def baguette(self, ctx, member: discord.Member = None):
        if member is None:
            rofl = ctx.author.avatar.url
            async with aiohttp.ClientSession() as session:
                request = await session.get(f'https://nekobot.xyz/api/imagegen?type=baguette&url={rofl}')
                dogjson = await request.json()
                await ctx.reply(dogjson['message'])
        else:
            rofl = member.avatar.url
            async with aiohttp.ClientSession() as session:
                request = await session.get(
                    f'https://nekobot.xyz/api/imagegen?type=baguette&url={rofl}')
                dogjson = await request.json() 
                await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clyde(self, ctx, *, message):
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=clyde&text={message}')
            dogjson = await request.json() 
        await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def distracted(self, ctx, member: discord.Member, user: discord.Member = None):
        hehe = user or ctx.author
        rofl = member.avatar.url
        lmfao = hehe.avatar.url
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=ship&user1={rofl}&user2={lmfao}'
            )
            dogjson = await request.json() 
            await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def captcha(self, ctx, message: str = None, member: discord.Member = None):
        member = member or ctx.author
        message = message or ctx.author.display_name
        lol = member.avatar.url
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=captcha&url={lol}&username={message}'
            )
            dogjson = await request.json() 
        await ctx.reply(dogjson['message'])


    @commands.command(aliases=["www"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whowouldwin(self, ctx, member: discord.Member, user: discord.Member = None):
        if user is None:
            rofl = ctx.author.avatar.url
            lmfao = member.avatar.url
            async with aiohttp.ClientSession() as session:
                request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=whowouldwin&user1={rofl}&user2={lmfao}'
                )
                dogjson = await request.json() 
                await ctx.reply(dogjson['message'])
        else:
            rofl = member.avatar.url
            lmfao = user.avatar.url
            async with aiohttp.ClientSession() as session:
                request = await session.get(f'https://nekobot.xyz/api/imagegen?type=whowouldwin&user1={rofl}&user2={lmfao}')
                dogjson = await request.json() 
                await ctx.reply(dogjson['message'])


    @commands.command(aliases=["cmm"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def changemymind(self, ctx, *, message):
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=changemymind&text={message}'
            )
            dogjson = await request.json() 
        await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lolice(self, ctx, member: discord.Member = None):

        if member is None: member = ctx.author

        rofl = member.avatar.url
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=lolice&url={rofl}')
            dogjson = await request.json()
            await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def iphone(self, ctx, member: discord.Member = None):

        if member is None: member = ctx.author

        rofl = member.avatar.url
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=iphonex&url={rofl}')
            dogjson = await request.json() 
            await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trap(self, ctx, member: discord.Member = None):

        if member is None: member = ctx.author

        rofl = member.avatar.url
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=trap&name={member.display_name}&author={ctx.message.author.display_name}&image={rofl}'
            )
            dogjson = await request.json()
            await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def awooify(self, ctx, member: discord.Member = None):

        if member is None: member = ctx.author

        rofl = member.avatar.url
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=awooify&url={rofl}')
            dogjson = await request.json()
            await ctx.reply(dogjson['message'])


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def phcomment(self, ctx, *, message):

        rofl = ctx.message.author.avatar.url
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=phcomment&image={rofl}&text={message}&username={ctx.message.author.display_name}'
            )
            dogjson = await request.json()
            await ctx.reply(dogjson['message'])



    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tweet(self, ctx, *, message: str, member: discord.Member = None):

        if member is None: member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://some-random-api.com/canvas/misc/tweet?avatar={member.avatar.url}&comment={message}&displayname={member.display_name}&username={member.display_name}&theme=dark"
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "tweet.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply("No card for you :(")
        
            await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trumptweet(self, ctx, *, message):
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://nekobot.xyz/api/imagegen?type=trumptweet&text={message}')
            dogjson = await request.json() 
        await ctx.reply(dogjson['message'])



    @commands.command(aliases=['scat'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sadcat(self, ctx, *, message):

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/sadcat?text={message}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'sadcat.jpeg'))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lgbt(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.com/canvas/misc/lgbt?avatar={member.avatar.url}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "lgbt.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply('No card for you :(')
                await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stupid(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.com/canvas/misc/its-so-stupid?avatar={member.avatar.url}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "stupid.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply('No card for you :(')
                await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pixel(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.com/canvas/misc/pixelate?avatar={member.avatar.url}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "pixel.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply('No card for you :(')
                await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tonikawa(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.com/canvas/misc/tonikawa?avatar={member.avatar.url}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "tonikawa.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply('No card for you :(')
                await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def genshin(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://some-random-api.com/canvas/misc/namecard?avatar={member.avatar.url}&username={member.display_name}&birthday=29/2&description=Ricky is my master."
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gi.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply("No card for you :(")
        
            await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def megamind(self, ctx, *, text):

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://some-random-api.com/canvas/misc/nobitches?no={text}"
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "mind.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply("No card for you :(")
        
            await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def oogway(self, ctx, *, text):

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://some-random-api.com/canvas/misc/oogway?quote={text}"
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "oogway.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply("No card for you :(")
        
            await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def oogway2(self, ctx, *, text):

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://some-random-api.com/canvas/misc/oogway2?quote={text}"
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "oogway2.png")
                    await ctx.reply(file=file)
                else:
                    await ctx.reply("No card for you :(")
        
            await session.close()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ytcomment(self, ctx, *, message, member: discord.Member = None):
        member = member or ctx.author
        lol = member.display_name
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.com/canvas/youtube-comment?username={lol}&comment={message}&avatar={member.avatar.url}&dark=true​') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "ytc.png")

                    await ctx.reply(file=file)
                else:
                    await ctx.reply('No card for you :(')
                await session.close()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clown(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/clown?image={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'clown.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ad(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/ad?image={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'ad.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uncover(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/uncover?image={member.avatar.url}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'uncover.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unforgivable(self, ctx, *, message):
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/unforgivable?text={message}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'unforgivable.jpeg'))


    @commands.command(aliases=['spitfa'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spittinfacts(self, ctx, *, message):
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/facts?text={message}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'facts.jpeg'))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def alert(self, ctx, *, message):
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/alert?text={message}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'alert.jpeg'))


async def setup(bot):
    await bot.add_cog(Canvas(bot))