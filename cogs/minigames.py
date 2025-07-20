import discord
import asyncio
import os
import akinator
import sys
import random

from collections import defaultdict
from discord.ext import commands
from random import shuffle

def h(*, randomcolor=False):
    return random.randint(0, 255**3)


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[
                condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def chooseWord():
    lines = open('data/wordbank.txt').read().splitlines()
    scrambled = [shuffleWord(word) for word in lines]
    return random.choice(scrambled)


def shuffleWord(word):
    original = word
    word = list(word)
    shuffle(word)
    return ''.join(word), original


def reset():
    global target
    target = ()


target = ()
scoreboard = {}

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

smoother = 'true'

global games
games = {}

def sort_dictionary(x):
    return {k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)}


class Minigames(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
        self.rounds = defaultdict(int)
        self.word_list = []


    async def cog_before_invoke(self, ctx):
        await ctx.channel.typing()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            eturn


    @commands.command(name="rps")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def rock_paper_scissors(self, context):
        choices = {0: "rock", 1: "paper", 2: "scissors"}
        reactions = {"🪨": 0, "🧻": 1, "✂": 2}
        embed = discord.Embed(
            title="Please choose. Rock, Paper, Scissors, Choose carefully, I never lost a match in my life :smirk:",
            color=0xEBD379)
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar.url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=0xEBD379)
            result_embed.set_author(name=context.author.display_name,
                                    icon_url=context.author.avatar.url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = h()
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = h()
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = h()
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = h()
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = h()
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late", color=0xEBD379)
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar.url)
            await choose_message.edit(embed=timeout_embed)


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def aki(self, ctx):
        aki = akinator.Akinator()

        q = aki.start_game()
        while aki.progression <= 80:

            embed = discord.Embed(
                title=f"{ctx.message.author.display_name}, here is your question",
                description=f'**{q}**',
                color=0xEBD379,
                timestamp=ctx.message.created_at)

            embed.set_footer(
                text="[yes (y) / no (n) / idk (i) / probably (p) / probably not (pn)]\n[back (b)]"
            )
            await ctx.send(embed=embed)
            a = await self.bot.wait_for(
                'message',
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            if a.content == "yep":
                a.content = "yes"
            elif a.content == "nop" or "nope":
                a.content == "no"
            elif a.content == "probably" or "proly":
                a.content == "p"
            elif a.content == "probably not" or "proly not":
                a.content == "pn"
            if a.content == "b":
                try:
                    q = aki.back()
                except akinator.CantGoBackAnyFurther:
                    pass
            else:
                try:
                    q = aki.answer(a.content)
                except akinator.InvalidAnswerError:
                    pass
        aki.win()
        em = discord.Embed(
            title=f"It's {aki.first_guess['name']}",
            description=f"({aki.first_guess['description']})! Was I correct?\n\n[yes (y) / no (n)]\n[back (b)]",
            color=0x0000)
        em.set_image(url=aki.first_guess['absolute_picture_path'])
        await ctx.send(embed=em)
        correct = await self.bot.wait_for(
            'message',
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        if correct.content.lower() == "yes" or correct.content.lower(
        ) == "y" or correct.content.lower() == "yep" or correct.content.lower(
        ) == "sure":
            await ctx.send(
                "Hell yeah! I am God incarnate")
        else:
            await ctx.send("D I E")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        channel = message.channel
        counting_channel_name = "counting"

        if channel.name == counting_channel_name:
            async for previous_message in channel.history(limit=1, before=message):
                previous_content = previous_message.content
                expected_number = int(previous_content) + 1

                if message.content.isdigit():
                    if int(message.content) == expected_number:
                        if self.last_member != message.author:
                            await message.add_reaction("✅")
                            self.last_member = message.author
                        else:
                            await message.add_reaction("❌")
                            await self.reset_counting_game(channel)
                    else:
                        await message.add_reaction("❌")
                        await self.reset_counting_game(channel)
                        await self.add_counting_mistake_role(message.author, channel)

    async def reset_counting_game(self, channel):
        await channel.purge(limit=None)
        await channel.send("The counting game has been reset. Start with 1!")
        self.last_member = None

    async def add_counting_mistake_role(self, member, channel, mistakes):
        role_name = "Lacks the ability to count ._."
        role = discord.utils.get(member.guild.roles, name=role_name)

        if not role:
            try:
                role = await member.guild.create_role(name=role_name, color=discord.Color.red(), reason="Counting game mistake role")
            except discord.Forbidden:
                print("Error: The bot does not have permission to create roles.")
                return

        if role not in member.roles:
            await member.add_roles(role)
            await member.send("Learn to count -_-")
            await channel.send(f"{member.mention}, you made a mistake in counting! You have been given the **'{role_name}'** role.", delete_after=5.0)
        else:
            await member.send("When will you learn to count -_-")
            await channel.send(f"{member.mention}, human beings should learn from their mistakes, wtf are you?", delete_after=5.0)

    @commands.command(aliases=["russian_roulette"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rr(self, ctx):
        responses = ["CLICK", "BANG"]
        survival_response = "CLICK"
        death_response = "BANG"
        
        if self.rounds[ctx.author.id] >= 3:
            await ctx.reply("You have already survived the maximum number of rounds. Play again later!")
            return

        result = random.choice(responses)
        if result == survival_response:
            self.rounds[ctx.author.id] += 1
            await ctx.reply(f"{ctx.author.mention}, {survival_response}\nYou have survived {self.rounds[ctx.author.id]} rounds!")
        else:
            self.rounds[ctx.author.id] = 0
            await ctx.reply(f"{ctx.author.mention}, {death_response}\nGame over! You lost all your survival streak!")


    @commands.command(aliases=['ttt'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tictactoe(self, ctx, p1: discord.Member, p2: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [
                ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:",
                ":white_large_square:"
            ]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn. `?place <1-9>` to start")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn. `?place <1-9>` to start")
        else:
            await ctx.send(
                "A game is already in progress! Finish it before starting a new one."
            )


    @commands.command()
    async def place(self, ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver == True:
                        await ctx.reply(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.reply("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.reply(
                        "Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile."
                    )
            else:
                await ctx.reply("It is not your turn.")
        else:
            await ctx.reply("Please start a new game using the tictactoe command.")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def scramble(self, ctx):

        global target
        if target:
            await ctx.reply(
                'The current word is {}. If you would like a different one, first ?reset and ?scramble again.'
                .format(target[0]))
        else:
            target = chooseWord()
            embed = discord.Embed(
            title= "Scramble",
            description= "Your scrambled word is: **{}**. Type **?guess your answer** to answer it or type **?reset**. Good Luck!".format(target[0]),
            color= h(),
            timestamp=ctx.message.created_at
            )
            await ctx.reply(embed=embed)


    @commands.command()
    async def guess(self, ctx, userGuess):

        global target
        global scoreboard

        if not target:
            await ctx.reply('There is no current word, please ?scramble to play')
            return

        if userGuess == target[1]:
            winner = ctx.author.name
            await ctx.reply('BINGO 🥵')
            if winner not in scoreboard:
                scoreboard[winner] = 0
            scoreboard[winner] += 5
            reset()


    @commands.command()
    async def reset(self, ctx):

        reset()
        await ctx.reply('Word has been reset, must ?scramble again for new word')


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def amongus(self, ctx):
    
        embed1 = discord.Embed(
            title="Who's the imposter?",
            description=
            "Find out who the imposter is, before the reactor breaks down! **30 seconds** 🕰️",
            color=0xEBD379)

        embed1.add_field(name='Red',
                        value='<:red:835107979048124437>',
                        inline=False)
        embed1.add_field(name='Blue',
                        value='<:blue:835107978196549663>',
                        inline=False)
        embed1.add_field(name='Green',
                        value='<:green:835107977341173781>',
                        inline=False)
        embed1.add_field(name='Pink',
                        value='<:pink:835107978701045791>',
                        inline=False)
        embed1.add_field(name='Orange',
                        value='<:orange:835107978109648927>',
                        inline=False)
        embed1.add_field(name='Yellow',
                        value='<:yellow:835107979400839168>',
                        inline=False)
        embed1.add_field(name='Black',
                        value='<:black:835107978038214686>',
                        inline=False)
        embed1.add_field(name='White',
                        value='<:white:835107978306256946>',
                        inline=False)
        embed1.add_field(name='Purple',
                        value='<:purple:835107977668984883>',
                        inline=False)
        embed1.add_field(name='Brown',
                        value='<:brown:835107978302062652>',
                        inline=False)
        embed1.add_field(name='Cyan',
                        value='<:cyan:835107979371216928>',
                        inline=False)
        embed1.add_field(name='Lime',
                        value='<:lime:835107978499457025>',
                        inline=False)
    
        msg = await ctx.reply(embed=embed1)

        emojis = {
            'Red': '<:red:835107979048124437>',
            'Blue': '<:blue:835107978196549663>',
            'Green': '<:green:835107977341173781>',
            'Pink': '<:pink:835107978701045791>',
            'Orange': '<:orange:835107978109648927>',
            'Yellow': '<:yellow:835107979400839168>',
            'Black': '<:black:835107978038214686>',
            'White': '<:white:835107978306256946>',
            'Purple': '<:purple:835107977668984883>',
            'Brown': '<:brown:835107978302062652>',
            'Cyan': '<:cyan:835107979371216928>',
            'Lime': '<:lime:835107978499457025>'
        }

        imposter = random.choice(list(emojis.items()))
        imposter = imposter[0]

        print(emojis[imposter])

        for emoji in emojis.values():
            await msg.add_reaction(emoji)

        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji) in emojis.values()

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                timeout=30.0,
                                                check=check)

        except asyncio.TimeoutError:
            description = "Reactor Meltdown. **{0}** was the imposter...".format(
                imposter)
            embed = discord.Embed(title="Defeat", description=description, color=0xEBD379)
            await ctx.reply(embed=embed)
        else:
            if str(self.reacted) == emojis[imposter]:
                description = "**{0}** was the imposter...".format(imposter)
                embed = discord.Embed(title="Victory", description=description, color=0xEBD379)
                await ctx.reply(embed=embed)

            else:
                for key, value in emojis.items():
                    if value == str(self.reacted):
                        description = "**{0}** was not the imposter...".format(key)
                        embed = discord.Embed(title="Defeat", description=description, color=0xEBD379)
                        await ctx.reply(embed=embed)
                        break


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def minesweeper(self, ctx, columns=None, rows=None, bombs=None):
        if columns is None or rows is None and bombs is None:
            if columns is not None or rows is not None or bombs is not None:
                await ctx.reply('That is not formatted properly or valid positive integers weren\'t used, the proper format is:\n`?minesweeper <columns> <rows> <bombs>`\n\n, You can give me nothing for random columns, rows, and bombs.')
                return
            else:
                columns = random.randint(4, 13)
                rows = random.randint(4, 13)
                bombs = columns * rows - 1
                bombs = bombs / 2.5
                bombs = round(random.randint(5, round(bombs)))
        try:
            columns = int(columns)
            rows = int(rows)
            bombs = int(bombs)
        except ValueError:
            await ctx.reply('That is not formatted properly or valid positive integers weren\'t used, the proper format is:\n`?minesweeper <columns> <rows> <bombs>`\n\n, You can give me nothing for random columns, rows, and bombs.')
            return
        if columns > 13 or rows > 13:
            await ctx.send(
                'The limit for the columns and rows are 13 due to discord limits...'
            )
            return
        if columns < 1 or rows < 1 or bombs < 1:
            await ctx.send('The provided numbers cannot be zero or negative...')
            return
        if bombs + 1 > columns * rows:
            await ctx.send(
                ':boom:**BOOM**, you have more bombs than spaces on the grid or you attempted to make all of the spaces bombs!'
            )
            return

        grid = [[0 for num in range(columns)] for num in range(rows)]

        loop_count = 0
        while loop_count < bombs:
            x = random.randint(0, columns - 1)
            y = random.randint(0, rows - 1)
            if grid[y][x] == 0:
                grid[y][x] = 'B'
                loop_count = loop_count + 1
            if grid[y][x] == 'B':
                pass

        pos_x = 0
        pos_y = 0
        while pos_x * pos_y < columns * rows and pos_y < rows:
            adj_sum = 0
            for (adj_y, adj_x) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1),
                                (-1, 1), (1, -1), (-1, -1)]:
                try:
                    if grid[adj_y + pos_y][
                            adj_x +
                            pos_x] == 'B' and adj_y + pos_y > -1 and adj_x + pos_x > -1:
                        adj_sum = adj_sum + 1
                except Exception as error:
                    pass
            if grid[pos_y][pos_x] != 'B':
                grid[pos_y][pos_x] = adj_sum
            if pos_x == columns - 1:
                pos_x = 0
                pos_y = pos_y + 1
            else:
                pos_x = pos_x + 1

        string_builder = []
        for the_rows in grid:
            string_builder.append(''.join(map(str, the_rows)))
        string_builder = '\n'.join(string_builder)
        string_builder = string_builder.replace('0', '||:zero:||')
        string_builder = string_builder.replace('1', '||:one:||')
        string_builder = string_builder.replace('2', '||:two:||')
        string_builder = string_builder.replace('3', '||:three:||')
        string_builder = string_builder.replace('4', '||:four:||')
        string_builder = string_builder.replace('5', '||:five:||')
        string_builder = string_builder.replace('6', '||:six:||')
        string_builder = string_builder.replace('7', '||:seven:||')
        string_builder = string_builder.replace('8', '||:eight:||')
        final = string_builder.replace('B', '||:bomb:||')

        percentage = columns * rows
        percentage = bombs / percentage
        percentage = 100 * percentage
        percentage = round(percentage, 2)

        embed = discord.Embed(title='\U0001F642 Minesweeper \U0001F635',
                            color=0xEBD379)
        embed.add_field(name='Columns:', value=columns, inline=True)
        embed.add_field(name='Rows:', value=rows, inline=True)
        embed.add_field(name='Total Spaces:', value=columns * rows, inline=True)
        embed.add_field(name='\U0001F4A3 Count:', value=bombs, inline=True)
        embed.add_field(name='\U0001F4A3 Percentage:',
                        value=f'{percentage}%',
                        inline=True)
        embed.add_field(name='Requested by:',
                        value=ctx.author.display_name,
                        inline=True)
        await ctx.reply(content=f'\U0000FEFF\n{final}', embed=embed)


    @commands.command(aliases=['slots'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slot(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.reply(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.reply(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.reply(f"{slotmachine} No match, you lost 😢")


async def setup(bot):
    await bot.add_cog(Minigames(bot))
