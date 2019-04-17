# This file hold the main writer rpg game

import random
import copy
from discord.ext import commands
import asyncio


class WriterRPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Save Profiles
    @staticmethod
    async def save_profile(profile):
        file_name = profile.name + ".txt"
        try:
            save_file_new = open(file_name, 'w')
            save_file_new.writelines(f"""{profile.name}\n""")
            save_file_new.writelines(f"""{profile.level}\n""")
            save_file_new.writelines(f"""{profile.exp}\n""")
            save_file_new.writelines(f"""{profile.hp}\n""")
            save_file_new.writelines(f"""{profile.atk}\n""")
            save_file_new.writelines(f"""{profile.block}\n""")
            save_file_new.writelines(f"""{profile.completed_stories}""")
            save_file_new.close()
        except IOError:
            save_file_new = open(file_name, "w")
            save_file_new.writelines(f"""{profile.name}\n""")
            save_file_new.writelines(f"""{profile.level}\n""")
            save_file_new.writelines(f"""{profile.exp}\n""")
            save_file_new.writelines(f"""{profile.hp}\n""")
            save_file_new.writelines(f"""{profile.atk}\n""")
            save_file_new.writelines(f"""{profile.block}\n""")
            save_file_new.writelines(f"""{profile.completed_stories}""")
            save_file_new.close()

    # Load profiles
    async def load_profile(self, user_name):
        profile = self.Profile()
        try:
            file_name = user_name + ".txt"
            save_file = open(file_name, "r")
            print("Loaded")

            profile.name = save_file.readline().replace('\n', '')
            profile.level = save_file.readline().replace('\n', '')
            profile.exp = save_file.readline().replace('\n', '')
            profile.hp = save_file.readline().replace('\n', '')
            profile.atk = save_file.readline().replace('\n', '')
            profile.block = save_file.readline().replace('\n', '')
            profile.completed_stories = save_file.readline().replace('\n', '')
            save_file.close()
            return profile
        except IOError:
            print("load_profile: IOError")
            profile = await self.create_profile(user_name)
            await self.save_profile(profile)
            return profile
        except LookupError:
            print("load_profile: IOError")
            profile = await self.create_profile(user_name)
            await self.save_profile(profile)
            return profile

    class Profile:
        def _init_(self, name, level, completed_stories, exp, atk, hp, block, eop):
            self.name = name
            self.level = level
            self.completed_stories = completed_stories
            self.exp = exp
            self.atk = atk
            self.hp = hp
            self.block = block
            self.eop = eop

    async def create_profile(self, p_name):
        profile = self.Profile()
        profile.name = p_name
        profile.level = 1
        profile.exp = 0
        profile.hp = 100
        profile.atk = 1
        profile.block = 0
        profile.completed_stories = 0
        profile.eop = "*"  # This is the End of profile mark. Use for marking a new profile in saved file
        return profile

    async def stats_display(self, profile, **kwargs):
        old_stats = kwargs.get('old_profile', self.Profile())
        lvl_up = kwargs.get('level_up', False)
        if not lvl_up:
            return (f"""`Name: {profile.name}`\n`Level: {profile.level}`\n""" +
                    f"""`Exp: {profile.exp}`\n`HP: {profile.hp}`\n`Atk: {profile.atk}`"""
                    + f"""\n`Block: {profile.block}`\n`Completed Stories: {profile.completed_stories}`\n""")
        else:
            return (f"""`{profile.name} has leveled up!`\n""" +
                    f"""```Old Level: {old_stats.level} - New Level: {profile.level}```\n""" +
                    f"""```Old HP: {old_stats.hp} - New HP: {profile.hp}```\n""" +
                    f"""```Old Atk: {old_stats.atk} - New Atk: {profile.atk}```\n""" +
                    f"""```Old Block: {old_stats.block} - New Block: {profile.block}```\n""")

    async def level_handler(self, profile):
        old_profile = copy.deepcopy(profile)

        if int(profile.exp) >= 100:
            profile.exp = 0
            profile.level = int(profile.level) + 1
            profile.hp = int(profile.hp) + random.randrange(25, 80)
            profile.atk = int(profile.atk) + random.randrange(1, 5)
            profile.block = int(profile.block) + random.randrange(1, 3)
            await self.save_profile(profile)
            new_stats = await self.stats_display(profile, old_profile=old_profile, level_up=True)
            return new_stats
        else:
            await self.save_profile(profile)
            new_stats = await self.stats_display(profile)
            return new_stats

    async def load(self, ctx):  # Use to find profiles
        profile = await self.load_profile(str(ctx))
        if not profile:
            profile = await self.create_profile(str(ctx))
            await self.save_profile(profile)
        return profile

    async def create_enemy(self, battle_lvl):
        class EProfile:
            def __init__(self, level, hp, atk, block):
                self.level = level
                self.hp = hp
                self.atk = atk
                self.block = block

        enemy = EProfile(1, 100, 1, 0)
        x = 1
        while x != battle_lvl:
            enemy.level = int(enemy.level) + 1
            enemy.hp += random.randrange(20, 60)
            enemy.atk += random.randrange(1, 3)
            enemy.block += random.randrange(1, 2)
            x += 1
        return enemy

    async def start_battle(self, **kwargs):
        ctx = kwargs.get('ctx', self)
        u_profile = kwargs.get('u_profile', self.Profile())
        e_profile = kwargs.get('e_profile', self.Profile())
        fight = kwargs.get('start_fight', False)
        time = kwargs.get('battle_time', 600)
        if not fight:
            await asyncio.sleep(5)
            return

        battle_time = time  # 600
        u_hp = int(u_profile.hp)
        while True:
            await ctx.send(f"""Battle started! Use your words to fight the enemy!""" +
                           f"""\nYou have {str(round((battle_time / 60), 2))} minutes!""")
            await asyncio.sleep(battle_time)
            await ctx.send(f"""{ctx.author.mention}, your time is up! Type your word count.\nYou have 30 seconds""" +
                           f""" to do so. (Please only type a number)""")
            words = 0
            try:
                msg = await self.bot.wait_for(event='message',
                                              check=lambda message: message.author == ctx.author, timeout=30)
                try:
                    msg = int(msg.content)
                    msg = abs(msg)
                except ValueError:
                    print('default to 0')
                    msg = 0
            except Exception:  # Ignore the underline here, this works as intended
                msg = 0

            words += msg
            u_atk = ((int(u_profile.atk) * 25) - (int(e_profile.block) * 15) +
                     (msg / 10) + (int(u_profile.completed_stories) * 2))
            u_atk = abs(u_atk)
            e_profile.hp -= u_atk
            await ctx.send(f"""You did {round(u_atk, 2)} damage!""")
            await asyncio.sleep(2)
            if e_profile.hp <= 0:
                await ctx.send("\n\nYou killed the enemy!")
                await asyncio.sleep(2)
                exp_gain = int(e_profile.level) - int(u_profile.level)
                if exp_gain <= 0:
                    exp_gain = 1
                exp_gain *= 10
                u_profile.exp = int(u_profile.exp) + exp_gain
                await ctx.send(f"""\n\nYou gained `{exp_gain}` exp!""")
                stats = await self.level_handler(u_profile)
                await ctx.send(stats)
                return
            else:
                await ctx.send(f"""\n\nThe enemy has `{round(e_profile.hp, 2)}` HP remaining.\nEnemy attacks!""")
                await asyncio.sleep(2)
                e_atk = ((int(e_profile.atk) * 30) - (int(u_profile.block) * 15) - (words / 10))
                if e_atk < 0:
                    e_atk = 0
                u_hp -= e_atk
                await ctx.send(f"""\n\nEnemy did {round(e_atk, 2)} damage!\nYou have `{round(u_hp, 2)}` health!""")
                await asyncio.sleep(2)
                if u_hp <= 0:
                    await ctx.send("\n\nYou lost the fight!")
                    return
                else:
                    await ctx.send(f"""\n\nThe battle continues!""")
                    await asyncio.sleep(2)
                    battle_time = time / 2  # 300

    # -^-^-^-^- Non-user functions ends here -^-^-^-^-
    # Commands below here

    @commands.command()
    async def create(self, ctx):
        """Creates a Writer-RPG profile if you don't have one."""
        try:
            file_name = str(ctx.author) + ".txt"
            save_file = open(file_name, "r")
            await ctx.send("You already have a Writer-RPG profile.")
            save_file.close()
        except IOError:
            await self.load_profile(str(ctx.author))
            await ctx.send("Writer-RPG profile created, use `^stats` to see your stats.")

    @commands.command()
    async def stats(self, ctx):
        """Shows the current stats of you Writer-RPG profile."""
        profile = await self.load(ctx.author)
        stats = await self.stats_display(profile)
        await ctx.send(stats)

    @commands.command()
    async def battle(self, ctx):
        """Starts a battle with a random enemy.
        Options:
            * Enter a number (minutes) for your fight
            * Add * for a guaranteed tough fight"""
        msg = ctx.message.content
        strong = False
        if '*' in str(msg):
            strong = True
        profile = await self.load_profile(str(ctx.author))
        battle_lvl = int(profile.level)
        if not strong:
            if battle_lvl < 3:
                battle_lvl = random.randrange((battle_lvl - 3), battle_lvl)
                if battle_lvl <= 0:
                    battle_lvl = 1
            else:
                battle_lvl = random.randrange((battle_lvl - 5), (battle_lvl + 5))
                if battle_lvl <= 0:
                    battle_lvl = 1
        else:
            battle_lvl = random.randrange((battle_lvl + 1), (battle_lvl + 5))
        enemy = await self.create_enemy(battle_lvl)
        # Time check
        time = 600
        for time in ctx.message.content.split():
            if time.isdigit():
                time = int(time)
            else:
                time = 10
        time *= 60
        print(f"""{time}""")
        await ctx.send(f"""Enemy Stats:\n`Level: {enemy.level}`\n`HP: {enemy.hp}`\n`Atk: {enemy.atk}`\n""" +
                       f"""`Block: {enemy.block}`""")
        await self.start_battle(ctx=ctx, u_profile=profile, e_profile=enemy, author=ctx.author, start_fight=True,
                                battle_time=time)

    @commands.command()  # Test command, remember to remove
    async def lvl(self, ctx):
        """A debug command that will be deleted"""
        profile = await self.load(ctx.author)
        stats = await self.level_handler(profile)
        await ctx.send(stats)


def setup(bot):
    bot.add_cog(WriterRPG(bot))
