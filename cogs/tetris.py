import discord
from discord.ext import commands
import asyncio
import os
import random

if not os.path.exists("highscores.txt"): 
    f = open("data/highscores.txt","w")
    f.close()

if not os.path.exists("monochrome.txt"): 
    f = open("data/monochrome.txt","w")
    f.close()  


figures = [
            [[1, 5, 9, 13], [4, 5, 6, 7]], 
            [[4, 5, 9, 10], [2, 6, 5, 9]], 
            [[6, 7, 9, 10], [1, 5, 6, 10]],
            [[0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8]],
            [[3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9], [1, 2, 6, 10]],
            [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]], 
            [[1, 2, 5, 6]],
]

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

array_4d = []
for figure in figures:
    array_3d = []
    for rotation in figure:
        array = [0 for i in range(16)]
        for digit in rotation:
            array[digit] = 1
        array_2d = list(chunks(array,4))
        array_3d.append(array_2d)
    array_4d.append(array_3d)
blocks = array_4d

next_block_images = [
    "https://i.imgur.com/wOSGSSa.png",
    "https://i.imgur.com/fl0W2g9.png",
    "https://i.imgur.com/gvwk6tL.png",
    "https://i.imgur.com/qetpxSR.png",
    "https://i.imgur.com/CxbSzSJ.png",
    "https://i.imgur.com/9XzmuWB.png",
    "https://i.imgur.com/zyNqMMo.png",
]

global games
games = {}

def sort_dictionary(x):
    return {k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)}

class Game:
    def __init__(self, user_id):
        self.game = [[0 for i in range(10)] for j in range(20)]
        self.next_block = Block(random.randint(0,6),0,3,0, self)
        self.ticks = 0
        self.message = None
        self.lines = 0
        self.level = 0
        self.score = 0
        self.game_over = False
        self.temp_points = 0
        self.user_id = user_id
        self.game_stopped = False
        self.monochrome = False

    async def tick(self):
        if self.game_stopped: return
        self.ticks += 1
        try:
            if self.ticks % (30-self.level*2) == 0 and not self.game_over:
                self.current_block.fall()
                await self.update_board()
            if self.game_over: await self.end_game()
        except: pass
        
        

    async def update_board(self):
        embed = self.message.embeds[0]
        embed.description = self.make_game()
        embed.set_thumbnail(url=next_block_images[self.next_block.blocktype])
        embed.clear_fields()
        embed.add_field(name="lines", value=self.lines, inline=True)
        embed.add_field(name="level", value=self.level, inline=True)
        embed.add_field(name="score", value=self.score, inline=True)
        await self.message.edit(embed=embed)

    async def end_game(self):
        self.game_stopped = True
        end_screen = "```"
        for i in range(9): end_screen += "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
        end_screen += "⬛⬛⬛⬛GAME ⬛⬛⬛⬛\n"
        end_screen += "⬛⬛⬛⬛OVER ⬛⬛⬛⬛\n"
        for i in range(9): end_screen += "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
        end_screen = end_screen[:-1]+"```"

        embed = self.message.embeds[0]
        embed.description = end_screen
        embed.set_thumbnail(url="https://i.imgur.com/UQYHC56.png")
        await self.message.edit(embed=embed)
        await self.message.clear_reactions()
        await self.update_scores()

    async def pause_game(self):
        self.game_stopped = True
        end_screen = "```"
        for i in range(9): end_screen += "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
        end_screen += "⬛⬛⬛⬛PAUSE⬛⬛⬛⬛\n"
        for i in range(10): end_screen += "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n"
        end_screen = end_screen[:-1]+"```"

        embed = self.message.embeds[0]
        embed.description = end_screen
        embed.set_thumbnail(url="https://i.imgur.com/wQVLUNS.png")
        await self.message.edit(embed=embed)
        await self.update_scores()

    def unpause_game(self):
        self.game_stopped = False

    async def update_scores(self):
        f = open("data/highscores.txt","r")
        text = f.readlines()
        f.close()
        scores = {}
        for line in text:
            split_text = line.replace("\n","").split(":")
            scores[split_text[0]] = int(split_text[1])
        try: old_score = scores[str(self.user_id)]
        except: old_score = 0
        
        if old_score < self.score:
            temp = {str(self.user_id) : self.score}
            scores.update(temp)
            new_scores = sort_dictionary(scores)

            embed = self.message.embeds[0]
            embed.clear_fields()
            embed.add_field(name="lines", value=self.lines, inline=True)
            embed.add_field(name="level", value=self.level, inline=True)
            embed.add_field(name="score", value=f"{self.score} (new highscore)", inline=True)
            await self.message.edit(embed=embed)

            score_text = ""
            for user,score in new_scores.items():
                score_text += f"{user}:{score}\n"
            f = open("data/highscores.txt","w")
            f.write(score_text)
            f.close()


    def new_block(self):
        self.ticks = 0
        self.remove_ghost_block()
        self.check_lines()
        self.current_block = self.next_block
        self.current_block.rotation = random.randint(0,len(blocks[self.current_block.blocktype])-1)
        self.current_block.y -= 1
        if (self.is_occupied(self.current_block)): self.current_block.y += 1
        if (self.is_occupied(self.current_block)): 
            self.current_block.rotation += 1
            if self.current_block.rotation >= len(blocks[self.current_block.blocktype]): self.current_block.rotation = 0
            if (self.is_occupied(self.current_block)):
                self.game_over = True
        self.place_block(self.current_block)
        self.next_block = Block(random.randint(0,6),0,3,0, self)


    def check_lines(self):
        lines = 0
        new_game = []
        
        row_index = 0
        for row in self.game:
            line_clear = True
            for digit in row:
                if digit == 0: line_clear = False

            if line_clear: lines += 1
            else: new_game.append(self.game[row_index])

            row_index += 1
        for i in range(lines):
            new_game.insert(0,[0 for i in range(10)])

        self.lines += lines
        score = self.level+1
        multipliers = [0,40,100,300,1200]
        score *= multipliers[lines]
        self.score += score
        self.level = int(self.lines/10)

        self.game = new_game


    def place_block(self,block_object):
        #render ghost block first
        block_object_2 = Block(block_object.blocktype,block_object.rotation,block_object.x,block_object.y, self)
        while not self.is_occupied(block_object_2): block_object_2.y += 1
        block_object_2.y -= 1
        row_index = 0
        for row in block_object_2.get_block():
            col_index = 0
            for col in row:
                if col == 1: self.game[block_object_2.y+row_index][block_object_2.x+col_index] = 8
                col_index += 1
            row_index += 1

        block = block_object.get_block()
        row_index = 0
        for row in block:
            col_index = 0
            for col in row:
                if col == 1: self.game[block_object.y+row_index][block_object.x+col_index] = block_object.blocktype+1
                col_index += 1
            row_index += 1
        

    def remove_block(self,block_object):
        self.remove_ghost_block()
        block = block_object.get_block()
        row_index = 0
        for row in block:
            col_index = 0
            for col in row:
                if col == 1: self.game[block_object.y+row_index][block_object.x+col_index] = 0
                col_index += 1
            row_index += 1

    def remove_ghost_block(self):
        new_game = []
        for row in self.game:
            new_row = []
            for digit in row:
                if digit == 8: new_row.append(0)
                else: new_row.append(digit)
            new_game.append(new_row)
        self.game = new_game

    def is_occupied(self, block_object):
        block = block_object.get_block()
        row_index = 0
        for row in block:
            col_index = 0
            for col in row:
                try:
                    if col == 1 and (block_object.x+col_index < 0 or block_object.x+col_index > 9 or block_object.y+row_index > 19 or block_object.y+row_index < 0 or (self.game[block_object.y+row_index][block_object.x+col_index] > 0 and self.game[block_object.y+row_index][block_object.x+col_index] < 8)): return True
                except: return True
                col_index += 1
            row_index += 1
        return False

    def make_game(self):
        if not self.monochrome: colors = ["⬛","⬜","🟥","🟩","🟦","🟧","🟪","🟨","🔳"]
        else: colors = ["⬛","⬜","⬜","⬜","⬜","⬜","⬜","⬜","🔳"]
        game_text = "```"
        for row in self.game:
            for digit in row:
                game_text += colors[digit]
            game_text += "\n"
        game_text = game_text[:-1]+"```"
        return game_text

class Block:
    def __init__(self, blocktype, rotation, x, y, game):
        self.blocktype = blocktype
        self.rotation = rotation
        self.x = x
        self.y = y
        self.game = game
        self.fall_points = 0

    def get_block(self):
        return blocks[self.blocktype][self.rotation]

    def rotate(self):
        self.game.remove_block(self)
        prev_rotation = self.rotation
        self.rotation += 1
        if self.rotation >= len(blocks[self.blocktype]): self.rotation = 0
        if (self.game.is_occupied(self)): 
            self.x += 1
            if (self.game.is_occupied(self)):
                self.x -= 2
                if (self.game.is_occupied(self)):
                    self.x += 1
                    self.y += 1
                    if (self.game.is_occupied(self)):
                        self.rotation = prev_rotation
                        self.y -= 1
        self.game.place_block(self)

    def move(self,units):
        self.game.remove_block(self)
        prev_x = self.x
        self.x += units
        if (self.game.is_occupied(self)): self.x = prev_x
        self.game.place_block(self)

    def fall(self):
        self.game.remove_block(self)
        self.y += 1
        create_new_block = False
        if (self.game.is_occupied(self)):
            self.y -= 1
            create_new_block = True
        self.game.place_block(self)
        if create_new_block:
            self.game.new_block()
            self.game.score += self.game.temp_points
            self.game.temp_points = 0
    
    def drop(self):
        self.game.remove_block(self)
        while not self.game.is_occupied(self):
            self.y += 1
        self.y -= 1
        self.game.place_block(self)
        self.game.new_block()
        self.game.score += self.game.temp_points
        self.game.temp_points = 0

class Tetris(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def tick(self):
        global games
        while True:
            for game in list(games.values()):
                try: await game.tick()
                except: print("oops")
            await asyncio.sleep(0.1)
            
    async def delete_dead_games(self):
        global games
        while True:
            users = []
            for user,game in games.items():
                if game.game_over and game.game_stopped: users.append(user)
            for user in users:
                del games[user]
            await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.tick())
        self.bot.loop.create_task(self.delete_dead_games())

    @commands.Cog.listener()
    async def on_message(self, message):
        global msg
        global games

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tetris(self, ctx):
        embed = discord.Embed(color=0xebd379,title="Tetris", description="- start\n- leaderboard\n- highscore\n- stop\n- pause\n- resume\n- monochrome\n- currentgames")
        embed.set_footer(text="example: ?start")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highscore(self, ctx):
            f = open("data/highscores.txt","r")
            text = f.readlines()
            f.close()
            scores = {}
            for line in text:
                split_text = line.replace("\n","").split(":")
                scores[split_text[0]] = split_text[1]
            scores = sort_dictionary(scores)
            try: 
                score = scores[str(ctx.author.id)]
            except: 
                await ctx.send("You've never played tetris in your life")

            score_list = list(scores.values())
            score_list.sort(reverse=True,key=lambda x: int(x))
            rank = score_list.index(score)+1
            await ctx.send(f"{ctx.author.mention}, your high score is {score} points (rank #{rank})")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def currentgames(self, ctx):
            '''
            amount_of_games = 0
            for game in games.values():
                if not game.game_over: amount_of_games += 1
            '''
            amount_of_games = len(games.values())
            await ctx.send(amount_of_games)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def monochrome(self, ctx):
            f = open("data/monochrome.txt","r")
            lines = f.readlines()
            f.close()

            user_id = str(ctx.author.id)+"\n"
            text = ""
            if user_id in lines:
                lines.remove(user_id)
                text = "You are no longer playing in monochrome"
                if ctx.author in games and not games[ctx.author].game_over:
                    games[ctx.author].monochrome = False
            else:
                lines.append(user_id)
                text = "You are now playing in monochrome"
                if ctx.author in games and not games[ctx.author].game_over:
                    games[ctx.author].monochrome = True

            f = open("data/monochrome.txt","w")
            f.writelines(lines)
            f.close()

            await ctx.send(text)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leaderboard(self, ctx):
            embed = discord.Embed(color=0xebd379,title="Tetris leaderboards")
            f = open("data/highscores.txt","r")
            text = f.readlines()
            f.close()
            highscores = {}
            for i in range(10):
                try:
                    split_text = text[i].replace("\n","").split(":")
                    usr = await self.bot.fetch_user(split_text[0])
                    username = str(usr)
                    highscores[username] = split_text[1]
                except:
                    break

            leaderboard = ""
            places = ["🥇 1st:","🥈 2nd:","🥉 3rd:","4th:","5th:","6th:","7th:","8th:","9th:","10th:"]
            for i in range(len(highscores)):
                if i < 3: leaderboard += "**"
                leaderboard += f"{places[i]} {list(highscores.keys())[i]} ({list(highscores.values())[i]} pts.)"
                if i < 3: leaderboard += "**"
                leaderboard += "\n"

            embed.description = leaderboard
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def start(self, ctx):
            if ctx.author in games and not games[ctx.author].game_over:
                await ctx.send("You're already playing tetris. you cant play two of them")
            else:
                games[ctx.author] = Game(ctx.author.id)
                game = games[ctx.author]
                game.new_block()
                
                f = open("data/monochrome.txt","r")
                text = f.readlines()
                f.close()
                if str(ctx.author.id)+"\n" in text: game.monochrome = True

                embed = discord.Embed(color=0xebd379, description=game.make_game())
                embed.set_author(name=f"{ctx.author.display_name}'s tetris", icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url=next_block_images[game.next_block.blocktype])
                embed.add_field(name="lines", value="0", inline=True)
                embed.add_field(name="level", value="0", inline=True)
                embed.add_field(name="score", value="0", inline=True)

                msg = await ctx.send(embed=embed)
                game.message = msg

                await msg.add_reaction("◀️")
                await msg.add_reaction("▶️")
                await msg.add_reaction("🔄")
                await msg.add_reaction("🔽")
                await msg.add_reaction("⏬")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stop(self, ctx):
            if ctx.author not in games or games[ctx.author].game_over:
                await ctx.send("You're already not playing tetris. you cant not play two of them")
            else:
                games[ctx.author].game_over = True
                await games[ctx.author].update_board()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pause(self, ctx):
            if ctx.author not in games or games[ctx.author].game_over:
                await ctx.send("You're already not playing tetris. you cant pause nothing")
            elif games[ctx.author].game_stopped:
                await ctx.send("You're already paused, use `?unpause`")
            else:
                await games[ctx.author].pause_game()
                await ctx.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unpause(self, ctx):
            if ctx.author not in games or games[ctx.author].game_over:
                await ctx.send("what")
            else:
                games[ctx.author].unpause_game()
                await ctx.delete()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global games
        global msg
        if user != self.bot.user and user in games and not games[user].game_stopped:
            game = games[user]
            await game.message.remove_reaction(reaction.emoji,user)
                
            if reaction.emoji == "🔄":
                game.current_block.rotate()
            if reaction.emoji == "◀️":
                game.current_block.move(-1)
            if reaction.emoji == "▶️":
                game.current_block.move(1)
            if reaction.emoji == "🔽":
                game.current_block.fall()
                game.temp_points += 1
            if reaction.emoji == "⏬":
                game.current_block.drop()
            
            await game.update_board()

async def setup(bot):
    await bot.add_cog(Tetris(bot))