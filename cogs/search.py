import discord
import aiohttp
import http
import random
import wikipedia
import requests
import datetime
import asyncio
from discord import File
from random import randint
from discord.ext import commands
from aiohttp import ClientSession 

def h(*, randomcolor=False):
    return random.randint(0, 255**3)


class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
            await ctx.channel.typing()
            
    async def cog_command_error(self, ctx, error):
            if isinstance(error, commands.CommandNotFound):
                return


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)  
    async def steam(self, ctx, *, search=None):
        await ctx.channel.typing()

        async with aiohttp.ClientSession() as session:
            request2 = await session.get(f'https://api.popcat.xyz/steam?q={search}')
            factjson = await request2.json()
            
        em = discord.Embed(title = f"**{factjson['name']}** - **{factjson['price']}**",
                            url = f"{factjson['website']}",
                            description = f"**Description**: {factjson['description']}\n\n**Developers**: {factjson['developers']}\n**Publishers**: {factjson['publishers']}",
                            timestamp = ctx.message.created_at,
                            color=0xEBD379
                        )
        em.set_thumbnail(url = f"{factjson['thumbnail']}")
        em.set_image(url = f"{factjson['banner']}")
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=em)

        
    @commands.command(aliases = ['anisearch'])
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def anime(self, ctx, *, message):
        await ctx.channel.typing()

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/anime?q={message}") as r:
                res = await r.json()

        em = discord.Embed(url = f"{res['data'][0]['url']}",
                        color=0xEBD379,
                        timestamp = ctx.message.created_at,
                        title = f"{res['data'][0]['title']}",
                        description = f"{res['data'][0]['synopsis']}")
        
        em.add_field(name="Japanese: ", value = f"{res['data'][0]['title_japanese']}", inline=False)    
        em.add_field(name="Synonyms: ", value = f"{res['data'][0]['title_synonyms']}", inline=False)
        em.add_field(name="Episodes: ", value = f"{res['data'][0]['episodes']}", inline=False)
        em.add_field(name="Status: ", value = f"{res['data'][0]['status']}", inline=False)
        em.add_field(name="Aired: ", value = f"{res['data'][0]['aired']['string']}", inline=False)
        em.add_field(name="Genre: ", value = f"{res['data'][0]['genres'][0]['name']}", inline=False)
        em.add_field(name="Duration: ", value = f"{res['data'][0]['duration']}", inline=False)
        em.add_field(name="Rating: ", value = f"{res['data'][0]['rating']}", inline=False)
        em.add_field(name="Score: ", value = f"{res['data'][0]['score']}", inline=False)
        em.add_field(name="Season: ", value = f"{res['data'][0]['season']}", inline=False)
        em.add_field(name="Trailer ", value = f"{res['data'][0]['trailer']['url']}", inline=False)
        em.set_thumbnail(url = f"{res['data'][0]['images']['jpg']['large_image_url']}") 

        await ctx.reply(embed=em)


    @commands.command(aliases=['mangasearch'])
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def manga(self, ctx, *, message):
        await ctx.channel.typing()

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/manga?q={message}") as r:
                res = await r.json()

        manga_info = res['data'][0]

        em = discord.Embed(
            url=manga_info['url'],
            color=0xEBD379,
            timestamp=ctx.message.created_at,
            title=manga_info['title'],
            description=manga_info['synopsis']
        )

        em.add_field(name="Japanese: ", value=manga_info['title_japanese'], inline=False)
        em.add_field(name="Synonyms: ", value=', '.join(manga_info['title_synonyms']), inline=False)
        em.add_field(name="Status: ", value=manga_info['status'], inline=False)
        em.add_field(name="Published: ", value=manga_info['published']['string'], inline=False)
        em.add_field(name="Score: ", value=manga_info['score'], inline=False)
        em.add_field(name="Rank: ", value=manga_info['rank'], inline=False)
        em.add_field(name="Popularity: ", value=manga_info['popularity'], inline=False)
        em.add_field(name="Members: ", value=manga_info['members'], inline=False)
        em.add_field(name="Favorites: ", value=manga_info['favorites'], inline=False)
        em.add_field(name="Genres: ", value=', '.join([genre['name'] for genre in manga_info['genres']]), inline=False)
        em.add_field(name="Themes: ", value=', '.join([theme['name'] for theme in manga_info['themes']]), inline=False)
        em.add_field(name="Authors: ", value=', '.join([author['name'] for author in manga_info['authors']]), inline=False)
        em.add_field(name="Serialization: ", value=manga_info['serializations'][0]['name'], inline=False)
        em.set_thumbnail(url=manga_info['images']['jpg']['large_image_url']) 

        await ctx.reply(embed=em)


    @commands.command(aliases=['randomanime'])
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def ranan(self, ctx):
        await ctx.channel.typing()

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.jikan.moe/v4/random/anime") as r:
                res = await r.json()

        anime_info = res['data']

        em = discord.Embed(
            url=anime_info['url'],
            color=0xEBD379,
            timestamp=ctx.message.created_at,
            title=anime_info['title'],
            description=anime_info['synopsis']
        )
        
        em.add_field(name="Japanese: ", value=anime_info['title_japanese'], inline=False)    
        em.add_field(name="Synonyms: ", value=', '.join(anime_info['title_synonyms']), inline=False)
        em.add_field(name="Episodes: ", value=anime_info['episodes'], inline=False)
        em.add_field(name="Status: ", value=anime_info['status'], inline=False)
        em.add_field(name="Aired: ", value=anime_info['aired']['string'], inline=False)
        
        genres = anime_info['genres']
        genre_value = genres[0]['name'] if genres else "N/A"
        em.add_field(name="Genre: ", value=genre_value, inline=False)
        
        em.add_field(name="Duration: ", value=anime_info['duration'], inline=False)
        em.add_field(name="Rating: ", value=anime_info['rating'], inline=False)
        em.add_field(name="Score: ", value=anime_info['score'], inline=False)
        em.add_field(name="Season: ", value=anime_info['season'], inline=False)
        em.add_field(name="Trailer ", value=anime_info['trailer']['url'], inline=False)
        em.set_thumbnail(url=anime_info['images']['jpg']['large_image_url']) 

        await ctx.reply(embed=em)


    @commands.command(aliases=['randommanga'])
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def ranman(self, ctx):
        await ctx.channel.typing()

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.jikan.moe/v4/random/manga") as r:
                res = await r.json()

        manga_info = res['data']

        em = discord.Embed(
            url=manga_info['url'],
            color=0xEBD379,
            timestamp=ctx.message.created_at,
            title=manga_info['title'],
            description=manga_info['synopsis']
        )

        em.add_field(name="Japanese: ", value=manga_info['title_japanese'], inline=False)
        em.add_field(name="Synonyms: ", value=', '.join(manga_info['title_synonyms']), inline=False)
        em.add_field(name="Status: ", value=manga_info['status'], inline=False)
        em.add_field(name="Published: ", value=manga_info['published']['string'], inline=False)
        em.add_field(name="Score: ", value=manga_info['score'], inline=False)
        em.add_field(name="Rank: ", value=manga_info['rank'], inline=False)
        em.add_field(name="Popularity: ", value=manga_info['popularity'], inline=False)
        em.add_field(name="Members: ", value=manga_info['members'], inline=False)
        em.add_field(name="Favorites: ", value=manga_info['favorites'], inline=False)
        em.add_field(name="Genres: ", value=', '.join([genre['name'] for genre in manga_info['genres']]), inline=False)
        em.add_field(name="Themes: ", value=', '.join([theme['name'] for theme in manga_info['themes']]), inline=False)
        em.add_field(name="Authors: ", value=', '.join([author['name'] for author in manga_info['authors']]), inline=False)
        em.add_field(name="Serialization: ", value=manga_info['serializations'][0]['name'], inline=False)
        em.set_thumbnail(url=manga_info['images']['jpg']['large_image_url']) 

        await ctx.reply(embed=em)


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def itunes(self, ctx, *, message):
        await ctx.channel.typing()

        str = message.replace(" ", "%20")

        async with aiohttp.ClientSession() as session:
            request2 = await session.get(f'https://api.popcat.xyz/itunes?q={str}')
            factjson = await request2.json()

        em = discord.Embed(color=0xEBD379,
                            timestamp = ctx.message.created_at,
                            title = f"{factjson['name']} - {factjson['artist']}",
                            url = f"{factjson['url']}")

        em.add_field(name = "Album: ", value = f"{factjson['album']}", inline = False)
        em.add_field(name = "Release: ", value = f"{factjson['release_date']}", inline = False)
        em.add_field(name = "Length: ", value = f"{factjson['length']}", inline = False)
        em.add_field(name = "Genre: ", value = f"{factjson['genre']}", inline = False)

        em.set_thumbnail(url = f"{factjson['thumbnail']}")

        await ctx.reply(embed=em)


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def imdb(self, ctx, *, message):
        await ctx.channel.typing()

        async with aiohttp.ClientSession() as r:
            async with r.get(f'https://api.popcat.xyz/imdb?q={message}') as cs:
                res = await cs.json()
    

        em = discord.Embed(color=0xEBD379,
                            timestamp = ctx.message.created_at,
                            title = f"{res['title']} - {res['year']}",
                            url = f"{res['imdburl']}")

        em.add_field(name = "Rating:", value = res['rating'], inline = False)
        em.add_field(name = "Metascore:", value = res['metascore'], inline = False)
        em.add_field(name = "Votes:", value = res['votes'], inline = False)
        em.add_field(name = "Box office:", value = res['boxoffice'], inline = False)
        em.add_field(name = "Release Date:", value = res['released'], inline = False)
        em.add_field(name = "Runtime:", value = res['runtime'], inline = False)
        em.add_field(name = "Genres:", value = res['genres'], inline = False)
        em.add_field(name = "Director:", value = res['director'], inline = False)
        em.add_field(name = "Writer:", value = res['writer'], inline = False)
        em.add_field(name = "Cast:", value = res['actors'], inline = False)
        em.add_field(name = "Language(s):", value = res['languages'], inline = False)
        em.add_field(name = "Awards:", value = res['awards'], inline = False)

        em.set_thumbnail(url = f"{res['poster']}")

        await ctx.reply(embed=em)


    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def randomwiki(self, ctx):
        await ctx.channel.typing()

        global current_language

        try:
            random_article = wikipedia.random(pages=1)

        except DisambiguationError:

            try:
                random_article = wikipedia.random(pages=1)
            except DisambiguationError:

                try:
                    random_article = wikipedia.random(pages=1)

                except DisambiguationError:
                    random_article = wikipedia.random(pages=1)

        pagecontent = wikipedia.page(random_article)
        pagetext = wikipedia.summary(random_article, sentences=5)

        try:
            thumbnail = pagecontent.images[randint(0, len(pagecontent.images))]

        except Exception as error:
            thumbnail = "https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(
            )
            print("Couldn't load {}".format(thumbnail))

        embed = discord.Embed(title=random_article,
                                color=0xEBD379,
                                description=pagetext +
                                "\n\n[Read further]({})".format(pagecontent.url))
        embed.set_thumbnail(url=thumbnail)
        await ctx.reply(embed=embed)


    @commands.command(aliases=['w', 'wiki'])
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def wikipedia(self, ctx, *, query: str):
        await ctx.channel.typing()
        sea = requests.get(
            ('https://en.wikipedia.org//w/api.php?action=query'
            '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
            ).format(query)).json()['query']

        if sea['searchinfo']['totalhits'] == 0:
            await ctx.reply('Sorry, your search could not be found.')
        else:
            for x in range(len(sea['search'])):
                article = sea['search'][x]['title']
                req = requests.get(
                    'https://en.wikipedia.org//w/api.php?action=query'
                    '&utf8=1&redirects&format=json&prop=info|images'
                    '&inprop=url&titles={}'.format(
                        article)).json()['query']['pages']
                if str(list(req)[0]) != "-1":
                    break
            else:
                await ctx.reply('Sorry, your search could not be found.')
                return
            article = req[list(req)[0]]['title']
            arturl = req[list(req)[0]]['fullurl']
            artdesc = requests.get(
                'https://en.wikipedia.org/api/rest_v1/page/summary/' +
                article).json()['extract']
            lastedited = datetime.datetime.strptime(req[list(req)[0]]['touched'],
                                                    "%Y-%m-%dT%H:%M:%SZ")
            embed = discord.Embed(title='**' + article + '**',
                                url=arturl,
                                description=artdesc,
                                color=0xEBD379)
            embed.set_footer(
                text='Wiki entry last modified',
                icon_url=
                'https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png'
            )
            embed.set_author(
                name='Wikipedia',
                url='https://en.wikipedia.org/',
                icon_url=
                'https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png'
            )
            embed.timestamp = lastedited
            await ctx.reply('**Search result for:** ***"{}"***:'.format(query), embed=embed)


    @commands.command(aliases=['dex'])
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def pokedex(self, ctx, *, args=None):
        try:
            if args == None:
                args = "pikachu"

            pokemon = args
            api = 'https://some-random-api.com//pokemon/pokedex?pokemon=' + pokemon
            json_data = requests.get(api).json()
            name = json_data["name"]
            ids = json_data["id"]
            types = json_data["type"]
            spe = json_data["species"]
            image = json_data["sprites"]
            desc = json_data["description"]
            evolu = json_data['family']
            abily = json_data['abilities']
            H = json_data['height']
            W = json_data['weight']
            G = json_data['generation']
            gender = json_data['gender']
            stat = json_data['stats']
            s = ", "
            com = s.join(types)
            spes = s.join(spe)
            abi = s.join(abily)
            evo = s.join(evolu['evolutionLine'])
            gen = s.join(gender)
            eg = json_data['egg_groups']
            egg = s.join(eg)

            em = discord.Embed(title=f"{name} #{ids}",
                                description=f":robot: : **{desc}**",
                                color=0x0000)
            em.set_thumbnail(url=image["animated"])
            em.add_field(name="Types", value=f"{com}", inline=True)
            em.add_field(name="Species", value=f"{spes}", inline=True)
            em.add_field(name="Ability", value=f"{abi}", inline=True)
            em.add_field(name="Evolution Stage",
                        value=f"The {evolu['evolutionStage']} Evolution",
                        inline=True)
            em.add_field(name="Evolution Line",
                        value=f"{evo if evo else 'No evolution line'}",
                        inline=False)
            em.add_field(name="Egg", value=f"{egg}", inline=False)
            em.add_field(name="Height", value=f"{H}", inline=True)
            em.add_field(name="Weight", value=f"{W}", inline=True)
            em.add_field(name="Gender", value=f"{gen}", inline=True)
            em.add_field(
                name="Stats :",
                value=
                f":heart: : {stat['hp']}\n:crossed_swords: : {stat['attack']}\n:shield: : {stat['defense']}\n:dash: : {stat['speed']}",
                inline=True)
            em.add_field(
                name="Sp Stats :",
                value=
                f"Sp :crossed_swords: : {stat['sp_atk']}\nSp️ ️:shield: : {stat['sp_def']}",
                inline=True)
            em.set_footer(
                text=
                f"This Pokemon Is From The {G} Generation\nTotal Stats : {stat['total']}"
            )
            await ctx.reply(embed=em)
        except KeyError:
            await ctx.reply(
                "That pokemon does not exist! make sure the spelling is correct")


    @commands.command(description='Defines most of the words out there', aliases=['meaning', 'define'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dictionary(self, ctx, *, word: str):
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            data = requests.get(url).json()
            definition = (data[0]['meanings'][0]['definitions'][0]['definition'])
            text = data[0]['phonetics'][0]['text']
            audio = data[0]['phonetics'][0]['audio']
            embed = discord.Embed(color=0xEBD379)
            embed.set_author(name=f"{word}")
            embed.add_field(name="Phonetics", value=f"Text = {text} \n[Audio]({audio})")
            embed.add_field(name="Definition", value=f"{definition}", inline=False)
            await ctx.reply(embed=embed)


    @commands.command(aliases=['periodictable'])
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def element(self, ctx, *, message):
        await ctx.channel.typing()

        async with aiohttp.ClientSession() as d:
            async with d.get(f"https://api.popcat.xyz/periodic-table?element={message}") as bs:
                deez = await bs.json()

        em = discord.Embed(color=0xEBD379,
                        timestamp = ctx.message.created_at,
                        title = deez['name'],
                        description=deez['summary'])
        em.add_field(name = "Symbol: ", value = f"{deez['symbol']}", inline = False)
        em.add_field(name = "Atomic Number: ", value = f"{deez['atomic_number']}", inline = False)
        em.add_field(name = "Atomic Mass: ", value = f"{deez['atomic_mass']}", inline = False)
        em.add_field(name = "Period: ", value = f"{deez['period']}", inline = False)
        em.add_field(name = "Phase: ", value = f"{deez['phase']}", inline = False)
        em.add_field(name = "Discovered By: ", value = f"{deez['discovered_by']}", inline = False)
        em.set_thumbnail(url = deez['image'])

        await ctx.reply(embed=em)

    @commands.command(aliases=['ly'])
    async def lyrics(self, ctx, *, search=None):
            if search is None:
                await ctx.send("Please provide a search argument.")
            else:
                async with aiohttp.ClientSession() as session:
                    request = await session.get(f'https://api.popcat.xyz/lyrics?song={search}')
                    dogjson = await request.json()

                title = dogjson.get('title', 'Unknown')
                artist = dogjson.get('artist', 'Unknown')
                lyrics = dogjson.get('lyrics', 'Lyrics not found.')

                em = discord.Embed(
                    title=f"{title} - {artist}",
                    description=lyrics,
                    timestamp=ctx.message.created_at,
                    color=0xEBD379
                )

                if dogjson.get('image'):
                    em.set_thumbnail(url=dogjson['image'])

                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)

                await ctx.reply(embed=em)

async def setup(bot):
    await bot.add_cog(Search(bot))