from discord.ext import commands
import discord
from cogs.tokens import MDOC_TOKEN

mdoc_id = MDOC_TOKEN


class MDOC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot command to add a master doc channel and create a follower role
    @commands.command()  # ^mdoc
    async def mdoc(self, ctx):
        """Creates a Master Doc channel and a follower role."""
        guild = ctx.message.guild
        owner = ctx.message.author
        name = str(ctx.message.author).lower()
        role_name = (name + "'s followers")
        check = str(owner).lower().replace("#", "")
        ch_lst = discord.utils.get(guild.channels, name=check)
        if ch_lst is None:
            overwrites = {
                owner: discord.PermissionOverwrite(read_messages=True, manage_channels=True, send_messages=True,
                                                   manage_messages=True, embed_links=True, attach_files=True,
                                                   manage_webhooks=True)
            }
            mdoc_category = self.bot.get_channel(mdoc_id)  # Remember to change this when creating stable version
            await guild.create_text_channel(name=str(owner).lower(), overwrites=overwrites, category=mdoc_category)
            await ctx.send("**Master Doc channel has been created!** "
                           "\n`Please note that changing the name of your channel " +
                           "is not allowed! If you do so you will get a warning and possibly have your channel "
                           "removed.`")
            guild = ctx.guild  # Creates a follower role for the user
            if discord.utils.get(guild.roles, name=role_name) is None:
                await guild.create_role(name=role_name, mentionable=True)
                await ctx.send(f"""\n**Follower role created! You may now have followers!**""")
        else:
            await ctx.send("You already have a Master Doc channel.")

    # Bot command to create follower role
    @commands.command()  # ^cf
    async def cf(self, ctx):
        """Creates a follower role. Only needed if your mdoc channel was made before but update 2.5."""
        name = str(ctx.message.author).lower()
        guild = ctx.guild
        role_name = (name + "'s followers")
        check = str(name).lower().replace("#", "")
        ch_lst = discord.utils.get(guild.channels, name=check)
        if ch_lst is not None:
            if discord.utils.get(guild.roles, name=role_name) is None:
                await guild.create_role(name=role_name, mentionable=True)
                await ctx.send("Follower role created! You may now have followers!")
            else:
                await ctx.send("You already have a follower role.")
        else:
            await ctx.send("You must have a Master Doc channel before you can create a follower role.")

    # Bot command to follow a user
    @commands.command()  # ^follow @user
    async def follow(self, ctx, member: discord.Member):
        """Follows the @mentioned user."""
        role = (str(member).lower() + "'s followers")
        check = discord.utils.get(ctx.guild.roles, name=role)
        if check in ctx.guild.roles:
            if check not in ctx.author.roles:
                await ctx.author.add_roles(check)
                await ctx.send("Following: " + str(member))
            else:
                await ctx.send("You're already following " + str(member) + ".")
        else:
            await ctx.send(str(member) + ", does not have a follow role set up.")

    # Bot command to unfollow a user
    @commands.command()  # ^unfollow @user
    async def unfollow(self, ctx, member: discord.Member):
        """Unfollows the @mentioned user."""
        role = str(member).lower() + "'s followers"
        check = discord.utils.get(ctx.guild.roles, name=role)
        if check in ctx.author.roles:
            await ctx.author.remove_roles(check)
            await ctx.send("You have unfollowed " + str(member))
        else:
            await ctx.send("You are not following " + str(member) + ".")

    # Show your followers
    @commands.command()  # ^mf
    async def mf(self, ctx):
        """Shows who's following you."""
        followers = []
        for member in ctx.message.guild.members:
            follower_name = discord.utils.get(member.guild.roles,
                                              name=(str(ctx.message.author) + "'s followers").lower())
            if follower_name in member.roles:
                followers.append(member.name)
        if not followers:
            await ctx.send("You have no followers.")
        else:
            await ctx.send(f"""Your followers are, {followers}""")


def setup(bot):
    bot.add_cog(MDOC(bot))
