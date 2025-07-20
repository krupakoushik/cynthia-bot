import discord
from discord.ext import commands

class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="AI", emoji="<:kayolove:1141011586115436654>"),
            discord.SelectOption(label="Canvas", emoji="<:jettlove:1141011572391678043>"),
            discord.SelectOption(label="Fun", emoji="<:neonlove:1141011566309933148>"),
            discord.SelectOption(label="Level", emoji="<:killjoylove:1141011554553303213>"),
            discord.SelectOption(label="Minigames", emoji="<:razelove:1141011539567063060>"),
            discord.SelectOption(label="Misc", emoji="<:omenlove:1141011559620018256>"),
            discord.SelectOption(label="Mod", emoji="<:phoenixlove:1141011590808875119>"),
            discord.SelectOption(label="Prefix", emoji="<:reynalove:1141011552804274206>"),
            discord.SelectOption(label="Reactions", emoji="<:sagelove:1141011543694254132>"),
            discord.SelectOption(label="Search", emoji="<:cypherlove:1141011579748491315>"),
            discord.SelectOption(label="Starboard", emoji="<:fadelove:1141011534399680607>"),
            discord.SelectOption(label="Ticket", emoji="<:viperlove:1141011548593197107>"),
            discord.SelectOption(label="Welcome", emoji="<:astralove:1141011598752882698>"),
        ]
        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):

        if self.values[0] == "AI":
            description = ("?chatbot <channel> | ?chatbotd")
            em = discord.Embed(title="?AI", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#AI")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Canvas":
            description = ("?ad [user] | ?alert <message> | ?awooify [user] | ?baguette [user] | ?captcha [user] [message] | ?changemymind (cmm) <message> | ?clown [user] | ?clyde <message> | ?comrade [user] | ?distracted <user1> [user2] | ?gay [user] | ?genshin [user] | ?glass [user] | ?gun [user] | ?horny [user] | ?iphone [user] | ?jail [user] | ?lgbt [user] | ?lolice [user] | ?megamind <message> | ?oogway <message> | ?oogway2 <message> | ?passed [user] | ?pet [user] | ?phcomment <message> | ?pixel [user] | ?sadcat <message> | ?simp [user] | ?spittinfacts <message> | ?stupid [user] | ?threat [user] | ?tonikawa [user] | ?trap [user] | ?triggered [user] | ?trumptweet <message> | ?tweet <message> [user] | ?uncover [user] | ?unforgivable <message> | ?wasted [user] | ?whowouldwin (www) <user1> [user2] | ?ytcomment <message> [user]")
            em = discord.Embed(title="?Canvas", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Canvas")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Fun":
            description = ("?afacts | ?affirm | ?aniquote | ?animals | ?binary (bi) <text> | ?biryani | ?bitcoin | ?bored | ?breakingbad (bb) | ?catface | ?choose <option1>, <option2>, ... | ?chucknorris	 | ?coffee | ?coinflip | ?color [#hexcode] | ?combine <name or user> <name or user> | ?dadjoke | ?dice | ?emojify <text> | ?emotes | ?enchanting | ?enlarge <emoji> | ?fact | ?fight [user] [weapon] | ?got | ?hotcalc [user] | ?howgay [user] | ?insult [user] | ?intellect <text> | ?internetrules | ?isthisforthat | ?joke | ?knock | ?lmgtfy <search> | ?mathadd <int> <int> | ?mathdiv <int> <int> | ?mathmult <int> <int> | ?mathrando <int> <int> | ?mathsqrt <int> | ?mathsub <int> <int> | ?magicball (8ball) | ?meme | ?morse <text> | ?nicememe | ?numberfact <number> | ?owo <text> | ?pickup | ?pokefusion | ?pp | ?quote | ?screenshot <search> | ?ship [user1] <user2> | ?sombra | ?spam | ?spellout <text> | ?spoilify <text> | ?sus [user] | ?thanosquote | ?thouart | ?trumpquote | ?twentyoneify (21ify) <text> | ?uselessfact | ?xkcd <random or int> | ?yearfact <int> | ?yesno <text> | ?yomama [user]")
            em = discord.Embed(title="?Fun", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Fun")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Level":
            description = ("?lb | ?levele [channel] | ?leveld | ?rank (lvl) | ?rewards | ?setrole <lvl> <role> | ?removerole <role>")
            em = discord.Embed(title="?Level", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Level")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Minigames":
            description = ("?aki | ?amongus | counting (not a command) | ?minesweeper [columns] [rows] [bombs] | ?rps | ?rr | ?scramble | ?slot | ?tetris | ?tictactoe (ttt)")
            em = discord.Embed(title="?Minigames", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Minigames")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Misc":
            description = ("?afk [reason] | ?av [user] | ?channelstats (cstats)	| ?members | ?mods | ?ping | ?pingadv | ?serverinfo | ?snipe | ?userinfo (whois) [user]")
            em = discord.Embed(title="?Misc", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Misc")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Mod":
            description = ("?ban <user> [reason] | ?cnick <user> <name> | ?kick <user> [reason] | ?lock | ?mute <user> | ?pin <id> | ?poll \"<question>\" <option1> <option2> ... | ?purge (clean) <int> | ?role <user> <role> | ?slowmode <int> | ?unban <user> | ?unlock | ?unmute <user> | ?userpurge <user> | ?warn <user> [reason] | ?warnings <user> | ?delwarn <user> <warn> | ?editwarn <user> <warn>")
            em = discord.Embed(title="?Mod", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Mod")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Prefix":
            description = ("?prefix | ?setprefix <prefix>")
            em = discord.Embed(title="?Prefix", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Prefix")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Reactions":
            description = ("?baka | ?boi | ?cry | ?cuddle | ?delet  | ?facepalm | ?feed | ?filth | ?heckoff | ?hug | ?kiss | ?laugh | ?lick | ?pat | ?poke | ?repost | ?slap | ?smug | ?tableflip | ?tickle | ?trigger | ?unflip | ?weirdshit | ?wink")
            em = discord.Embed(title="?Reactions", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Reactions")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Search":
            description = ("?anime <name> | ?dictionary <word> | ?element <element> | ?imdb <title> | ?itunes <song> | ?ly <song> | ?manga <name> | ?pokedex <name> | ?ranan | ?ranman | ?randomwiki | ?steam <name> | ?wiki <name>")
            em = discord.Embed(title="?Search", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Search")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Starboard":
            description = ("?starboard <channel>")
            em = discord.Embed(title="?Starboard", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Starboard")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Ticket":
            description = ("?ticket <category id> | ?ticketdel | ?close")
            em = discord.Embed(title="?Ticket", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Ticket")
            await interaction.response.edit_message(embed=em, view=SelectView())

        elif self.values[0] == "Welcome":
            description = ("?welcome <channel> [msg] [upload image for bg] | ?welcomedel")
            em = discord.Embed(title="?Welcome", description=description, color=0xEBD379, url="https://krupakoushik.github.io/cynthia/commands.html#Welcome")
            await interaction.response.edit_message(embed=em, view=SelectView())

class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(with_app_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        description = (
            "**Default Prefix:** `?`\n\n"
            "**Useful Links:**\n"
            "[Invite](https://discord.com/oauth2/authorize?client_id=1118220952556286013&permissions=37377489763703&scope=applications.commands%20bot)\n"
            "[Website](https://krupakoushik.github.io/cynthia/)\n"
            "[Commands](https://krupakoushik.github.io/cynthia/commands.html)\n"
            "[Super Active Server ;-;](https://discord.com/invite/TvXvxC7zhM)\n\n"
            "**Other Links:**\n"
            "[Top.gg](https://top.gg/bot/1118220952556286013)\n"
            "[Top.gg(Vote)](https://top.gg/bot/1118220952556286013/vote)\n"
        )
        em = discord.Embed(title="The coolest multi-purpose bot in town :)", description=description, color=0xEBD379)
        await ctx.send(embed=em, view=SelectView())



async def setup(bot):
    await bot.add_cog(Help(bot))
