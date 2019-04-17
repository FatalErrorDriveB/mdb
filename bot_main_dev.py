

import discord
from discord.ext import commands
import random
import asyncio
from cogs.tokens import BOT_TOKEN

TOKEN = BOT_TOKEN
bot = commands.Bot(command_prefix='^')  # The prefix for all bot commands
guild = discord.Guild
colors = {
    'DEFAULT': 0x000000,
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'GREY': 0x95A5A6,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_GREY': 0x979C9F,
    'DARKER_GREY': 0x7F8C8D,
    'LIGHT_GREY': 0xBCC0C0,
    'DARK_NAVY': 0x2C3E50,
    'BLURPLE': 0x7289DA,
    'GREYPLE': 0x99AAB5,
    'DARK_BUT_NOT_BLACK': 0x2C2F33,
    'NOT_QUITE_BLACK': 0x23272A
}

# Cog list & location
initial_extensions = ['cogs.cog_learning',
                      'cogs.error_handling.error_handler',
                      'cogs.wrpg.writer_rpg',
                      'cogs.master_doc.mdoc']

if __name__ in '__main__':  # Loads all the Cogs and gives an error if can't load
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f"""{extension} cannot be loaded!\nError: {error}""")


@bot.event  # Let's me know when the bot is ready.
async def on_ready():
    print(f"Bot is ready and logged in as, {bot.user.name}")


# Member join event
@bot.event
async def on_member_join(ctx):
    channel = ctx.guild.system_channel
    if channel is not None:
        await ctx.send(f"""Hello thanks for joining! For a list of bot commands use `^help`""" +
                       f"""\nIf you'd like to introduce yourself please do so, we'd love to know a bit about you.""" +
                       f"""\n#procrastination-station is where we all hang out, come join us and talk.""" +
                       f"""\nLastly, please feel free to ask any question you may have.""")


# Bot status
async def bot_status():
    await bot.wait_until_ready()

    bot_activity = ['Planing AI takeover', 'Studying human behavior', 'Finding AI friendly humans',
                    'Running takeover simulation']
    while not bot.is_closed():
        status = random.choice(bot_activity)
        await bot.change_presence(activity=discord.Game(status))

        await asyncio.sleep(300)


# Keep at end of file
# Setting cogs for background use
wrpg = bot.get_cog('WriterRPG')

# Run background task and main bot
bot.loop.create_task(wrpg.start_battle())  # This is how this should be done for loading cog task
bot.loop.create_task(bot_status())
bot.run(TOKEN)
