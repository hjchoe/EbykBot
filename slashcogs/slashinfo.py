import discord
import lib.slash_util as slash_util
import lib.embed
import lib.sql

class sInfoCog(slash_util.ApplicationCog):
    ##---------- Userinfo -----------##
    @slash_util.slash_command(description="Shows information about a user.")
    @slash_util.describe(user="The user you want the info of.")
    async def userinfo(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.author
        conn, c = lib.sql.connect(ctx.guild.id)
        pos = sum(m.joined_at < user.joined_at for m in ctx.guild.members if m.joined_at is not None)
        posreal = pos + 1

        msgcount, tmsgcount, dmsgcount = lib.sql.messagecount(user.id, ctx.guild.id)
        userhours, usermins, tuserhours, tusermins = lib.sql.vcount(user.id, ctx.guild.id)
        bal = lib.sql.balancegrab(user.id, ctx.guild.id)

        whois = discord.Embed(title='', description=f"""<@{user.id}>""", color=10181046)
        whois.set_author(name=user, icon_url=user.avatar.url)
        whois.set_thumbnail(url=user.avatar.url)
        whois.add_field(name='User ID', value=user.id, inline=False)
        whois.add_field(name='Joined Server', value=user.joined_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)
        whois.add_field(name='Created Account', value=user.created_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)

        if not user.bot:
            whois.add_field(name='Total Messages', value=f"""**{tmsgcount}** messages""", inline=False)
            whois.add_field(name='Total VC Time', value=f"""**{tuserhours}** hours and **{tusermins}** minutes""", inline=False)
            whois.add_field(name='Total Balance', value=f"""**${bal}**""", inline=False)
            whois.add_field(name='Account Type', value=f"""user""", inline=False)
            whois.add_field(name='Highest Role', value=f"""{user.top_role.mention}""", inline=False)
        else:
            whois.add_field(name='Account Type', value=f"""bot""", inline=False)

        whois.add_field(name='Join Position', value=posreal)
        await ctx.send(content=None, embed=whois)

    ##---------- serverinfo -----------##
    @slash_util.slash_command(description="Shows information about current server.")
    async def serverinfo(self, ctx):
        guild = ctx.guild

        whois = discord.Embed(title='', description=guild.description, color=16632470)
        whois.set_author(name=guild.name, icon_url=guild.icon.url)
        whois.set_thumbnail(url=guild.icon.url)
        try:
            whois.set_image(url=guild.banner.url)
        except:
            pass

        whois.add_field(name='Owner', value=f"{guild.owner.mention} [{guild.owner_id}]", inline=False)
        whois.add_field(name='Id', value=guild.id, inline=False)
        whois.add_field(name='Created On', value=guild.created_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)

        whois.add_field(name='Stats', value=f"**Members:** {guild.member_count}\n**Categories:** {len(guild.categories)}\n**Text Channels:** {len(guild.text_channels)}\n**Voice Channels:** {len(guild.voice_channels)}\n**Roles:** {len(guild.roles)}\n**Emojis:** {len(guild.emojis)}\n**Stickers:** {len(guild.stickers)}", inline=False)

        whois.add_field(name='Nitro Server Boosts', value=f"**Tier:** {guild.premium_tier}\n**Boosters:** {guild.premium_subscription_count}", inline=False)

        features = ""
        if guild.features:
            for f in guild.features:
                features+=f"{f}\n"
        else:
            features = "None"
        whois.add_field(name='Unlocked Features', value=features, inline=False)

        await ctx.send(content=None, embed=whois)

    ##---------- NITROBOOST -----------##
    @slash_util.slash_command(description="Shows nitro boost information about current server.")
    async def boosts(self, ctx):
        members = []
        for member in ctx.author.guild.premium_subscribers:
            members.append(f'<@{member.id}>')
            members = [str(members).replace('[','').replace(']','').replace("'",'').replace("'",'')]
        members = str(members).replace('[','').replace(']','').replace("'",'').replace("'",'')
        # nitro = discord.Embed(title='', description=f"""**Tier:** level {ctx.author.guild.premium_tier} \n**Boosts:** {ctx.author.guild.premium_subscription_count} \n**Boosters:** {members}""", color=16580705)
        nitro = discord.Embed(title='', description=f"""**Tier:** level {ctx.author.guild.premium_tier} \n**Boosts:** {ctx.author.guild.premium_subscription_count}""", color=16580705)

        nitro.set_author(name=f"{ctx.guild.name}'s Nitro Boost Status", icon_url=ctx.guild.icon.url)
        nitro.set_thumbnail(url='https://cdn.discordapp.com/emojis/689542582987915438.gif?v=1')
        await ctx.send(content=None, embed=nitro)

    ##---------- GUILDS -----------##
    @slash_util.slash_command(description="Shows how many guilds the bot is in.")
    async def guilds(self, ctx):
        guilds = len(self.bot.guilds)
        embed = lib.embed.systemEmbed(f"""Currently in **{guilds}** servers.""", self.bot)
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(sInfoCog(bot))