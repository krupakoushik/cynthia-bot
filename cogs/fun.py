import discord
import random
import aiohttp
import asyncpraw
import re
import requests
import json
import urllib.parse
import io
import asyncio

import easy_pil
from easy_pil import Canvas, Editor, Font, load_image_async
from discord import File

from random import randrange
from PIL import Image
from discord.ext.commands import clean_content
from aiohttp import ClientSession
from discord.ext import commands
from random import choice, randint


def h(*, randomcolor=False):
  return random.randint(0, 255**3)

def strip_global_mentions(self, message, ctx=None):
    if ctx:
        perms = ctx.message.channel.permissions_for(self, ctx.message.author)
        if perms.mention_everyone:
            return message
    remove_everyone = re.compile(re.escape("@everyone"), re.IGNORECASE)
    remove_here = re.compile(re.escape("@here"), re.IGNORECASE)
    message = remove_everyone.sub("everyone", message)
    message = remove_here.sub("here", message)
    return message


reddit = asyncpraw.Reddit(client_id='QXnPQRii0fYR0g', client_secret="bvgICfa3oSSQ1uL0FQoR79l34wFO9Q", username="Affectionate_Ad7863", password="krupak3005", user_agent="Affectionate_Ad7863")

encode_morse ={
    "1":".----",
    "2":"..---",
    "3":"...--",
    "4":"....-",
    "5":".....",
    "6":"-....",
    "7":"--...",
    "8":"---..",
    "9":"----.",
    "0":"-----",
    "A":".-",
    "B":"-...",
    "C":"-.-.",
    "D":"-..",
    "E":".",
    "F":"..-.",
    "G":"--.",
    "H":"....",
    "I":"..",
    "J":".---",
    "K":"-.-",
    "L":".-..",
    "M":"--",
    "N":"-.",
    "O":"---",
    "P":".--.",
    "Q":"--.-",
    "R":".-.",
    "S":"...",
    "T":"-",
    "U":"..-",
    "V":"...-",
    "W":".--",
    "X":"-..-",
    "Y":"-.--",
    "Z":"--..",
    ".":".-.-.-",
    ",":"--..--",
    ":":"---...",
    "?":"..--..",
    "'":".----.",
    "-":"-....-",
    "/":"-..-.",
    "@":".--.-.",
    "=":"-...-",
    " ":"/"
}


class Fun(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()
        
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        subreddit = await reddit.subreddit("memes")
        all_subs = []
        top = subreddit.top(limit = 50)

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)
        
        url = random_sub.url
        text = random_sub.title

        em = discord.Embed(title = text,
                        url = url, 
                        color=0xEBD379,
                        timestamp=ctx.message.created_at)
        em.set_image(url=url)
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar.url)
        
            
        await ctx.reply(url)

    @commands.command()
    async def sus(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.message.author
        susness = randrange(101)
        convertedsus = str(susness)
        convertedmember = str(member)
        embed=discord.Embed(title="SUSSY BAKA", description=convertedmember + " is `" + convertedsus + "%` sus")
        await ctx.send(embed=embed)

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def insult(self, ctx, boi: discord.Member = None):
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://evilinsult.com/generate_insult.php?lang=en&type=json') as r:
                res = await r.json()

        if boi is ctx.author:
            await ctx.reply('It\'s quite peculiar that you have an interest in being insulted by a bot...')
        elif boi is None:
            await ctx.reply("Your attempt to insult nobody reveals your lack of intelligence...")
        elif self.bot.user in ctx.message.mentions:
            await ctx.reply("**YOU ARE A BITCH FOR TRYING THIS!**")
        else:
            await ctx.reply(f"{boi.mention}, {res['insult']}")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def spam(self, ctx):
            
            await ctx.reply(file=discord.File("assets/imgs/spam.png"))


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 6000, commands.BucketType.user) 
    async def internetrules(self, ctx):
            
            await ctx.reply(file=discord.File("data/InternetRules.txt"))  


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sombra(self, ctx):
            
            await ctx.reply("```\n                       :PB@Bk:                         \n                   ,jB@@B@B@B@BBL.                     \n                7G@B@B@BMMMMMB@B@B@Nr                  \n            :kB@B@@@MMOMOMOMOMMMM@B@B@B1,              \n        :5@B@B@B@BBMMOMOMOMOMOMOMM@@@B@B@BBu.          \n     70@@@B@B@B@BXBBOMOMOMOMOMOMMBMPB@B@B@B@B@Nr       \n   G@@@BJ iB@B@@  OBMOMOMOMOMOMOM@2  B@B@B. EB@B@S     \n   @@BM@GJBU.  iSuB@OMOMOMOMOMOMM@OU1:  .kBLM@M@B@     \n   B@MMB@B       7@BBMMOMOMOMOMOBB@:       B@BMM@B     \n   @@@B@B         7@@@MMOMOMOMM@B@:         @@B@B@     \n   @@OLB.          BNB@MMOMOMM@BEB          rBjM@B     \n   @@  @           M  OBOMOMM@q  M          .@  @@     \n   @@OvB           B:u@MMOMOMMBJiB          .BvM@B     \n   @B@B@J         0@B@MMOMOMOMB@B@u         q@@@B@     \n   B@MBB@v       G@@BMMMMMMMMMMMBB@5       F@BMM@B     \n   @BBM@BPNi   LMEB@OMMMM@B@MMOMM@BZM7   rEqB@MBB@     \n   B@@@BM  B@B@B  qBMOMB@B@B@BMOMBL  B@B@B  @B@B@M     \n    J@@@@PB@B@B@B7G@OMBB.   ,@MMM@qLB@B@@@BqB@BBv      \n       iGB@,i0@M@B@MMO@E  :  M@OMM@@@B@Pii@@N:         \n          .   B@M@B@MMM@B@B@B@MMM@@@M@B                \n              @B@B.i@MBB@B@B@@BM@::B@B@                \n              B@@@ .B@B.:@B@ :B@B  @B@O                \n                :0 r@B@  B@@ .@B@: P:                  \n                    vMB :@B@ :BO7                      \n                        ,B@B                           ```")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def coffee(self, ctx):
        

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://coffee.alexflipnote.dev/random.json') as r:
                res = await r.json()

        em = discord.Embed(title = '**Coffee Supremacy** 🛐',
                            color = h(),
                            timestamp = ctx.message.created_at
                            )
        em.set_image(url = f"{res['file']}")
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar.url)

        await ctx.reply(res['file'])

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def biryani(self, ctx):
        

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://biriyani.anoram.com/get') as r:
                res = await r.json()

        em = discord.Embed(title = '**Biryani Supremacy** 🛐',
                            color = h(),
                            timestamp = ctx.message.created_at
                            )
        em.set_image(url = f"{res['image']}")
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar.url)

        await ctx.reply(res['image'])

    @commands.command(aliases = ['8ball'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def magicball(self, ctx, *, message):
        

        Affirmations = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes."]
        NonCommital = ["Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again."]
        Negative = ["Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
        dict = [Affirmations, NonCommital, Negative]
        dicts = random.choice(dict)
        reply = random.choice(list(dicts))
        await ctx.reply(reply)


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def affirm(self, ctx):
        

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.affirmations.dev/') as r:
                res = await r.json()

        await ctx.reply(res['affirmation'])


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def got(self, ctx):
        

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://api.gameofthronesquotes.xyz/v1/random') as r:
                res = await r.json()

        em = discord.Embed(title = res['sentence'],
                            description = f"- {res['character']['name']}",
                            color = h(),
                            timestamp = ctx.message.created_at
                            )
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar.url)

        await ctx.reply(embed=em)


    @commands.command(aliases=['bbq', 'bb'])
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def breakingbad(self, ctx):
            

            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://api.breakingbadquotes.xyz/v1/quotes') as r:
                    quotes = await r.json()

                quote = quotes[0]
                text = quote['quote']
                author = quote['author']

                em = discord.Embed(
                    title=text,
                    description=f"- {author}",
                    color=0xEBD379
                )

            await ctx.reply(embed=em)


    @commands.command(aliases=['21ify'])
    @commands.cooldown(1, 5, commands.BucketType.user)   
    async def twentyoneify(self, ctx, *, input:str):
        
        await ctx.reply(input.replace("O", "Ø").replace("o", "ø"))

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def intellect(self, ctx, *, msg: str):
        intellectify = ""
        words = msg.split()
        for word in words:
            intellectify += random.choice([word.upper(), word.lower()]) + " "
        
        await ctx.reply(intellectify.rstrip())



    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def morse(self, ctx, *, msg:str):
        
        encoded_message = ""
        for char in list(msg.upper()):
            encoded_message += encode_morse[char] + " "
            await ctx.send(encoded_message)


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def spellout(self, ctx, *, msg:str):
        
        await ctx.reply(" ".join(list(msg.upper())))


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bored(slef, ctx):
        

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'http://www.boredapi.com/api/activity/') as r:
                res = await r.json()

        em = discord.Embed(title = "Imagine having no friends :rofl:",
                        description = f"**Activity**: {res['activity']}\n**Type**: {res['type']}\n**Participants**: {res['participants']}\n**Link**: {res['link']}",
                        color = h(),
                        timestamp = ctx.message.created_at
                        )
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar.url)

        await ctx.reply(embed=em)


    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def emotes(self, ctx):
        
        msg = ''
        for emoji in ctx.guild.emojis:
            if len(msg) + len(str(emoji)) > 1000:
                embed = discord.Embed(description=msg, color=0xEBD379)
                await ctx.send(embed=embed)
                msg = ''
            msg += str(emoji)

        embed = discord.Embed(description=msg, color=0xEBD379)
        await ctx.send(embed=embed)


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def ship(self, ctx, name2: discord.Member, name1: discord.Member = None):
        

        if name1 is None: name1 = ctx.message.author

        shipnumber = random.randint(0, 100)
        
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(random.choice(["Friendzone ;(", 'Just "friends"', '"Friends"',"Little to no love ;(", "There's barely any love ;(", "Ahh the classic ``one sided love``"]))
        
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(random.choice(["Still in the friendzone", "Still in that friendzone ;(","There's not a lot of love there... ;("]))
        
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!","But there's a small bit of love somewhere", "I sense a small bit of love!","But someone has a bit of love for someone..."]))
        
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(random.choice(["There's a bit of love there!","There is a bit of love there...","A small bit of love is in the air..."]))
        
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO", "It appears one sided!","There's some potential!", "I sense a bit of potential!","There's a bit of romance going on here!","I feel like there's some romance progressing!","The love is getting there..."]))
        
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(random.choice(["I feel the romance progressing!","There's some love in the air!","I'm starting to feel some love!"]))
        
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(random.choice(["There is definitely love somewhere!","I can see the love is there! Somewhere...","I definitely can see that love is in the air"]))
        
        elif 80 < shipnumber <= 90:
            status = "Above average! {}".format(random.choice(["Love is in the air!", "I can definitely feel the love","I feel the love! There's a sign of a match!","There's a sign of a match!", "I sense a match!","A few things can be imporved to make this a match made in heaven!"]))
        
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(random.choice(["It's a match!", "There's a match made in heaven!","It's definitely a match!", "Love is truely in the air!","Love is most definitely in the air!"]))

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        if shipnumber <= 10:
            gif =  "https://media.tenor.com/images/8eb3ea6f8b8e05115a37df84ba03144a/tenor.gif"
        if 10 < shipnumber <=30:
            gif= "https://media.tenor.com/images/d9f4ebad1365272d2605a1a5151d501a/tenor.gif"
        if 30 < shipnumber <=50:
            gif = "https://media.tenor.com/images/12414d69b8a99bd6dc19275363e17554/tenor.gif"
        if 50 < shipnumber <= 70:
            gif = "https://64.media.tumblr.com/09efd576d1e31d6dbf2a66eaa07ef6af/tumblr_n52l5bmodz1tt23n5o1_500.gif"
        if 70 < shipnumber <= 100:
            gif = "https://media.tenor.com/images/d85ef0ba33daf46de0838eba3efe8d08/tenor.gif"

        lol = name1.display_name
        lmfao = name2.display_name
        emb = (discord.Embed(color=shipColor, title="Love test for:", description="**{0}** and **{1}** {2}".format(lol, lmfao, random.choice([":sparkling_heart:", ":heart_decoration:", ":heart_exclamation:", ":heartbeat:", ":heartpulse:", ":blue_heart:", ":green_heart:", ":purple_heart:", ":revolving_hearts:", ":yellow_heart:", ":two_hearts:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_thumbnail(url=f'{gif}')
        emb.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=emb)


    @commands.command(aliases=['pf'])
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def pokefusion(self, ctx):
        
        poke1 = random.randrange(1, 151)
        poke2 = random.randrange(1, 151)
        
        embed = discord.Embed(title="WHO'S THAT POKEMON⁉️ :eyes:", colour=h())
        embed.set_image(url=f"https://images.alexonsager.net/pokemon/fused/{poke1}/{poke1}.{poke2}.png")
        embed.set_footer(text= f"https://pokemon.alexonsager.net/{poke2}/{poke1}")
        
        await ctx.reply(embed=embed)

    @commands.command(aliases=['q'])
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def quote(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.reply(quote)


    @commands.command(aliases=["coin"])
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def coinflip(self, ctx):
        
        choices = ["Heads", "Tails"]
        rancoin = random.choice(choices)
        await ctx.reply(f"||{rancoin}||")


    @commands.command(aliases=['aquote'])
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def aniquote(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/animu/quote')
            r = await request.json()

        embed = discord.Embed(
            title=f"**{r['sentence']}**",
            description=
            f"**Said By**: {r['character']}\n**From**: {r['anime']}",
            color=0xEBD379)
        await ctx.reply(embed=embed)


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def pp(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        length = random.randrange(15)
        await ctx.reply(f"{member.display_name}'s pp size is...\n\n 8{'='*length}D")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def combine(self, ctx, name1: clean_content, name2: clean_content):
        name1letters = name1[:round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2):]
        ship = "".join([name1letters, name2letters])
        emb = discord.Embed(
            title=':heartpulse: __**MATCHMAKING**__ :heartpulse:',
            color=0xEBD379,
            description=f"**:heart: {name1} + {name2} :heart:**\n\n **:heart: `{ship}` :heart:**"
        )
        emb.set_image(url='https://media.giphy.com/media/eg3f90cy2Mc6yVRWyR/giphy.gif')
        await ctx.reply(embed=emb)


    @commands.command(aliases=['gayrate'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def howgay(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        gayness = random.randint(0, 100)

        if gayness <= 33:
            gayStatus = random.choice([
                "No homo", "Wearing socks", '"Only sometimes"', "Straight-ish",
                "No homo bro", "Girl-kisser", "Hella straight"
            ])
            gayColor = 0xFFC0CB
        
        elif 33 < gayness < 66:
            gayStatus = random.choice([
                "Possible homo", "My gay-sensor is picking something up",
                "I can't tell if the socks are on or off", "Gay-ish",
                "Looking a bit homo", "lol half  g a y",
                "safely in between for now"
            ])
            gayColor = 0xFF69B4
        
        else:
            gayStatus = random.choice([
                "LOL YOU GAY XDDD FUNNY", "HOMO ALERT",
                "MY GAY-SENSOR IS OFF THE CHARTS", "STINKY GAY", "BIG GEAY",
                "THE SOCKS ARE OFF", "HELLA GAY"
            ])
            gayColor = 0xFF00FF
        
        emb = discord.Embed(description=f"Gayness for **{user.display_name}**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
        emb.set_author(name="Gay-Scanner™",icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png")
        await ctx.reply(embed=emb)


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dadjoke(self, ctx):
        url = "https://dad-jokes.p.rapidapi.com/random/joke/png"
        headers = {
            'x-rapidapi-key': "7e5f86fba6msh7fe4c99b035a89dp14ea65jsn92e1ad331cde",
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                r = await response.json()
            await ctx.reply(f"**{r['body']['setup']}**\n\n||{r['body']['punchline']}||")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bitcoin(self, ctx):
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
        await ctx.reply(f"Bitcoin price is: ${response['bpi']['USD']['rate']}")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enlarge(self, ctx,  emoji: discord.PartialEmoji = None):
        if not emoji:
            await ctx.reply("You need to provide an emoji!")
        else:
            await ctx.reply(emoji.url)


    @commands.command(aliases=['hex', 'colour'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def color(self, ctx, inputcolor=''):
        if inputcolor == '':
            randgb = lambda: random.randint(0, 255)
            hexcode = '%02X%02X%02X' % (randgb(), randgb(), randgb())
            rgbcode = str(tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4)))
            heximg = Image.new("RGB", (64, 64), '#' + hexcode)
            heximg.save("color.png")          
            await ctx.reply('`Hex: #' + hexcode + '`\n`RGB: ' + rgbcode + '`', file=discord.File('color.png'))
        else:
            if inputcolor.startswith('#'):
                hexcode = inputcolor[1:]
                if len(hexcode) == 8:
                    hexcode = hexcode[:-2]
                elif len(hexcode) != 6:
                    await ctx.reply('Make sure hex code is this format: `#7289DA`')
                rgbcode = str(tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4)))
                heximg = Image.new("RGB", (64, 64), '#' + hexcode)
                heximg.save("color.png")
                await ctx.reply('`Hex: #' + hexcode + '`\n`RGB: ' + rgbcode + '`', file=discord.File('color.png'))

            else:
                await ctx.reply('Make sure hex code is this format: `#7289DA`')

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lmgtfy(self, ctx, *, searchquery: str):
        await ctx.reply('<https://lmgtfy.com/?iie=1&q={}>'.format(
            urllib.parse.quote_plus(searchquery)))

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emojify(self, ctx, *, text: str):
        emojified = '⬇ Copy and paste this: ⬇\n'
        formatted = re.sub(r'[^A-Za-z ]+', "", text).lower()
        if text == '':
            await ctx.reply('Remember to say what you want to convert!')
        else:
            for i in formatted:
                if i == ' ':
                    emojified += '     '
                else:
                    emojified += ':regional_indicator_{}: '.format(i)
            if len(emojified) + 2 >= 2000:
                await ctx.reply('Your message in emojis exceeds 2000 characters!')
            if len(emojified) <= 25:
                await ctx.reply('Your message could not be converted!')
            else:
                await ctx.reply('`' + emojified + '`')


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spoilify(self, ctx, *, text: str):
        spoilified = '⬇ Copy and paste this: ⬇\n'
        if text == '':
            await ctx.reply('Remember to say what you want to convert!')
        else:
            for i in text:
                spoilified += '||{}||'.format(i)
            if len(spoilified) + 2 >= 2000:
                await ctx.reply('Your message in spoilers exceeds 2000 characters!')
            if len(spoilified) <= 4:
                await ctx.reply('Your message could not be converted!')
            else:
                await ctx.reply('`' + spoilified + '`')


    @commands.command(aliases=['howhot', 'hot'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        hehe = user or ctx.author
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.reply(f"Perfectly precise calculations\n\n**{hehe.name}** is **{hot:.2f}%** hot {emoji}")


    @commands.command(aliases=["thanos"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def thanosquote(self, ctx):

        quotes = [
            "The end is near.",
            "You're strong. But I could snap my fingers, and you'd all cease to exist.",
            "Fun isn't something one considers when balancing the universe. But this… does put a smile on my face.",
            "Stark… you have my respect. I hope the people of Earth will remember you.",
            "When I'm done, half of humanity will still exist. Perfectly balanced, as all things should be. I hope they remember you.",
            "You should have gone for the head.",
            "I know what it's like to lose. To feel so desperately that you're right, yet to fail nonetheless. Dread it. Run from it."
            + " Destiny still arrives. Or should I say, I have.",
            "Going to bed hungry. Scrounging for scraps. Your planet was on the brink of collapse. I was the one who stopped that."
            +
            " You know what's happened since then? The children born have known nothing but full bellies and clear skies. It's a paradise.",
            "I ignored my destiny once, I can not do that again. Even for you. I'm sorry little one.",
            "With all six stones, I can simply snap my fingers, they would all cease to exist. I call that mercy.",
            "The hardest choices require the strongest wills.",
            "A soul for a soul.", "Balanced, as all things should be.",
            "Fun isn't something one considers when balancing the universe. But this… does put a smile on my face.",
            "I know what it's like to lose. To feel so desperately that you're right, yet to fail nonetheless. Dread it. Run from it. Destiny still arrives. Or should I say, I have.",
            "You could not live with your own failure, and where did that bring you? Back to me.",
            "I am... inevitable.", "I don't even know who you are.",
            "I used the stones to destroy the stones. It nearly killed me, but the work is done. It always will be. I'm inevitable.",
            "You're not the only one cursed with knowledge.",
            "Reality is often disappointing.",
            "A small price to pay for salvation."
        ]

        await ctx.reply(f"{random.choice(quotes)}")


    @commands.command(aliases=['trump'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trumpquote(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.tronalddump.io/random/quote')
            trump = await request.json()
            await ctx.reply(trump['value'])


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def catface(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://nekos.life/api/v2/cat')
            trump = await request.json()

            await ctx.reply(trump['cat'])


    @commands.command(aliases=["chuck"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chucknorris(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.chucknorris.io/jokes/random')
            trump = await request.json()

            await ctx.reply(trump['value'])


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enchanting(self,ctx):
        embed = discord.Embed(
            title='__**Minecraft Enchanting Table Font**__',
            description=
            "**a => ᔑ\n\n b => ʖ\n\n c => ᓵ\n\n d => ↸\n\n e => ᒷ\n\n f => ⎓\n\n g => ⊣\n\n h => ⍑\n\n i => ╎\n\n j => ⋮\n\n k => ꖌ\n\n l => ꖎ\n\n m => ᒲ\n\n n => リ\n\n o => 𝙹\n\n p => !¡\n\n q => ᑑ\n\n r => ∷\n\n s => ᓭ\n\n t => ℸ\n\n u => ⚍\n\n v => ⍊\n\n w => ∴\n\n x => /\n\n y => ||\n\n z => ⨅**",
            color=0xEBD379,
            timestamp=ctx.message.created_at)
        embed.set_thumbnail(
            url='https://media.giphy.com/media/i7NLlLUaaG9u8/giphy.gif')

        await ctx.reply(embed=embed)

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yomama(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://api.yomomma.info')
            dogjson = await request.json()
        await ctx.reply(dogjson['joke'])

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yesno(self, ctx, *, message: str):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://yesno.wtf/api/')
            dogjson = await request.json()

        embed = discord.Embed(title=f"__**{message}**__",
                                color=0x0000,
                                timestamp=ctx.message.created_at)
        embed.add_field(name="**Answer**: ", value=dogjson['answer'])
        embed.set_image(url=dogjson['image'])
        await ctx.reply(embed=embed)\


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dice(self, ctx):

        sides = ["1", "2", "3", "4", "5", "6"]

        lol = random.choice(sides)

        await ctx.reply(f"**{lol}**")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def thouart(self, ctx, member: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            request = await session.get('http://quandyfactory.com/insult/json/')
            dogjson = await request.json()

        await ctx.reply(dogjson['insult'])

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pickup(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f'https://api.popcat.xyz/pickuplines')
            dogjson = await request.json() 
        await ctx.reply(dogjson['pickupline'])


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joke(self, ctx):

        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.com/joke')
            r = await request.json()
            await ctx.reply(r['joke'])

    @commands.command(aliases=['ss'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def screenshot(self, ctx, *, message):

        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(
                    f'https://api.popcat.xyz/screenshot?url=https://{message}'
            ) as wastedImage:
                imageData = io.BytesIO(await wastedImage.read())

                await wastedSession.close()

                await ctx.reply(file=discord.File(imageData, 'ss.jpeg'))


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def xkcd(self, ctx,  *, searchterm: str):
        apiUrl = 'https://xkcd.com{}info.0.json'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(apiUrl.format('/')) as r:
                js = await r.json()
                if ''.join(searchterm) == 'random':
                    randomComic = random.randint(0, js['num'])
                    async with cs.get(apiUrl.format('/' + str(randomComic) +
                                                    '/')) as r:
                        if r.status == 200:
                            js = await r.json()
                comicUrl = 'https://xkcd.com/{}/'.format(js['num'])
                date = '{}.{}.{}'.format(js['day'], js['month'], js['year'])
                msg = '**{}**\n{}\nAlt Text:```{}```XKCD Link: <{}> ({})'.format(
                    js['safe_title'], js['img'], js['alt'], comicUrl, date)
                await ctx.reply(msg)

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def knock(self, ctx):

        knock_Jokes = [
            'Amos.\nAmos who?\nA mosquito bit me!',
            'Andy.\nAndy who?\nAnd he bit me again.',
            'Yetta.\nYetta who?\nYetta nother mosquito!',
            'Notta.\nNotta who?\nNotta nother mosquito!',
            'Abe Lincoln.\nAbe Lincoln who?\nAww, come on! Don’t you know who Abe Lincoln is?',
            'Lettuce.\nLettuce who?\nLettuce in and I’ll tell you!',
            'Ida\nIda who?\nIda like to be your friend!',
            'Warrior.\nWarrior who?\nWarrior been all my life!',
            'Olive.\nOlive who?\nOlive you!',
            'Adore.\nAdore who?\nAdore is between us open it up.',
            'A little boy.\nAlittle boy who?\nA little boy who can’t reach the doorbell.',
            'Anita.\nAnita who?\nAnita nother minute to think it over.',
            'Hutch.\nHutch who?\nBless you!!!',
            'Tank.\nTank who?\nYou’re welcome!',
            'Goliath.\nGoliath who?\nGoliath down, you look sleepy!!',
            'Lego.\nLego who?\nLego of me and I’ll tell you!',
            'T-Rex.\nT-Rex who?\nThere is a T-Rex at your door and you want to know his name!?!',
            'Woo.\nWoo who?\nDon’t get too excited, it’s just a joke!',
            'Police.\nPolice who?\nPol-e-s-e open the door!',
            'Nunya.\nNunya who?\nNunya business!',
            'Radio.\nRadio who?\nRadio not here I come!',
            'Howard.\nHoward who?\nHoward you like a big kiss!',
            'Issac\nIssac Who?\nIssac (I sick) of Knock Knock Jokes!',
            'Cow says.\nCow says who?\nNo, a cow says mooooo!',
            'Europe.\nEurope who?\nNo I’m not!',
            'Adore.\nAdore who?\nAdore is between us. Open up!',
            "Amish!\nAmish who?\nYou're not a shoe!",
            "Alfie\nAlfie who?\nAlfie terrible if you leave!",
            "Amish\nAmish Who?\nAw How sweet. I miss you too.",
            "Amanda\nAmanda who?\nA man da fix your sink!",
            "Al\nAl who?\nAl give you a kiss if you open this door!",
            "Avenue\nAvenue who?\nAvenue knocked on this door before?",
            "Alien\nAlien who?\nJust how many aliens do you know?",
            "Britney Spears\nBritney Spears who?\nKnock, knock - oops i did it again.",
            "Ben\nBen who?\Ben knocking on this door all morning, let me in!",
            "CD\nCD who?\nCD guy on your doorstep?",
            "Cows go\nCow's go who?\nNo, silly. Cows go Moo!",
            "Cook\nCook who?\nYes you are!",
            "Cheese\nCheese who?\nCheese a nice girl",
            "Chick!\nChick who?\nChick your oven, I can smell burning!",
            "Cupid!\nCupid who?\nCupid quiet in there.",
            "Déja.\nDéja who?\nKnock knock.",
            "Doris\nDoris who?\nThe Doris locked, why do you think I'm knocking?",
            "Dish\nDish who?\nDish is a nice place!",
            "Egg\nEgg who?\nEggstremely disappointed you still don’t recognize me.",
            "Emma\nEmma who?\nEmma bit cold out here, can you let me in?",
            "Barbie\nBarbie who?\nBarbie Q Chicken!",
            "Oswald\nOswald who?\nOswald my gum!",
            "Nuisance\nNuisance who?\nWhat’s nuisance yesterday",
            "Dwight\nDwight who?\nDwight way is better than the wrong way!",
            "Norma Lee\nNorma Lee who?\nNorma Lee I have my key, can you let me in?",
            "A little old lady\nA little old lady who?\nI didn’t know you could yodel!",
            "Dozen\nDozen who?\nDozen anybody want to let me in?",
            "Avenue\nAvenue who?\nAvenue knocked on this door before?",
            "Ice Cream\nIce Cream who?\nIce Cream if you don't let me in!",
            "Bed\nBed who?\nBed you can not guess who I am.",
            "Abby\nAbby who?\nAbby birthday to you!",
            "Rufus\nRufus who?\nRufus the most important part of your house.",
            "Wanda\nWanda who?\nWanda hang out with me right now?",
            "Ho-ho.\nHo-Ho who?\nHo-Ho You know, your Santa impression could use a little work.",
            "Mary and Abbey\nMary and Abbey who?\nMary Christmas and Abbey New Year!",
            "Carmen\nCarmen who?\nCarmen let me in already!",
            "Ya\nYa Who?\nYa I’m excited to see you too!",
            "Scold\nScold Who?\nScold outside—let me in!",
            "I'm Robin\nI'm Robin Who?\nI'm Robin you! Hand over your cash!",
            "Irish\nIrish who?\nIrish you a Merry Christmas!",
            "Otto\nOtto who?\nOtto know whats taking you so long!",
            "Needle\nNeedle who?\nNeedle little help gettin in the door.",
            "Luke\nLuke who?\nLuke through the keyhole to see!",
            "Justin\nJustin who?\nJustin the neighborhood and thought Id come over.",
            "Europe\nEurope who?\nEurope no, you are a poo",
            "To\nTo who?\nTo Whom.", "Etch\nEtch who?\nGod Etch You!",
            "Mikey\nMickey who?\nMickey doesnt fit through this keyhole"
        ]

        await ctx.reply(f"Knock Knock\nWho's there?\n{random.choice(knock_Jokes)}")


    @commands.command(aliases=['itft'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def isthisforthat(self, ctx):
        async with ClientSession() as session:
            async with session.get(
                    'http://itsthisforthat.com/api.php?text') as response:
                r = await response.text()
                await ctx.reply(f"**{r}**")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nicememe(self, ctx):
        await ctx.reply(f"http://niceme.me")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fight(self, ctx, user: str = None, *, weapon: str = None):


        fight_results = [
            "and it was super effective!", "but %user% dodged it!",
            "and %user% got obliterated!", "but %attacker% missed!",
            "but they killed each other!",
            "and it wiped out everything within a five mile radius!",
            "but in a turn of events, they made up and became friends. Happy ending!",
            "and it worked!", "and %user% never saw it coming.",
            "but %user% grabbed the attack and used it against %attacker%!",
            "but it only scratched %user%!", "and %user% was killed by it.",
            "but %attacker% activated %user%'s trap card!",
            "and %user% was killed!"
        ]

        if user is None or user.lower(
        ) == ctx.author.mention or user == ctx.author.name.lower(
        ) or ctx.guild is not None and ctx.author.nick is not None and user == ctx.author.nick.lower(
        ):
            await ctx.reply(
                "{} fought themself but only ended up in a mental hospital!".
                format(ctx.author.mention))
            return
        if weapon is None:
            await ctx.reply(
                "{0} tried to fight {1} with nothing so {1} beat the breaks off of them!"
                .format(ctx.author.mention, user))
            return
        await ctx.reply("{} used **{}** on **{}** {}".format(
            ctx.author.mention, weapon, user,
            random.choice(fight_results).replace("%user%", user).replace(
                "%attacker%", ctx.author.mention)))


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def owo(self, ctx, *, text: commands.clean_content):
        replacement_table = {  # Thanks luna for the rep table!
            r'[rl]': 'w',
            r'[RL]': 'W',
            r'n([aeiou])': 'ny\\1',
            r'N([aeiou])': 'Ny\\1',
            r'ove': 'uv'
        }
        kao = ["OwO", "UwU", ":3"]
        r = random.randint(0, len(kao) - 1)
        for regex, replace_with in replacement_table.items():
            text = re.sub(regex, replace_with, text)

        await ctx.reply(text + " " + kao[r])


    @commands.command(aliases=['bi'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def binary(self, ctx, *, args):
        try:
            name = args
            api = 'https://some-random-api.com/binary?text=' + name
            json_data = requests.get(api).json()
            biner = json_data['binary']
            await ctx.reply(biner)

        except:
            a = await ctx.reply("**Cannot Find What You Mean 0_0**")
            await asyncio.sleep(1)
            await a.edit("Please Try Again **With An ALPHABET Word**")


    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def choose(self, ctx, *, choices):
        bruh = (choices.split(","))
        await ctx.reply(random.choice(bruh))


async def setup (bot):
    await bot.add_cog (Fun(bot))