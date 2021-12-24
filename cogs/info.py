import discord
from discord.ext import commands
import lib.embed
import lib.sql

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##---------- Userinfo -----------##
    @commands.guild_only()
    @commands.command(aliases=['whois'])
    async def userinfo(self, ctx, member : discord.Member=None):
        if member is None:
            member = ctx.author
        conn, c = lib.sql.connect(ctx.guild.id)
        pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
        posreal = pos + 1

        msgcount, tmsgcount, dmsgcount = lib.sql.messagecount(member.id, ctx.guild.id)
        userhours, usermins, tuserhours, tusermins = lib.sql.vcount(member.id, ctx.guild.id)
        bal = lib.sql.balancegrab(member.id, ctx.guild.id)

        whois = discord.Embed(title='', description=f"""<@{member.id}>""", color=10181046)
        whois.set_author(name=member, icon_url=member.avatar.url)
        whois.set_thumbnail(url=member.avatar.url)
        whois.add_field(name='User ID', value=member.id, inline=False)
        whois.add_field(name='Joined Server', value=member.joined_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)
        whois.add_field(name='Created Account', value=member.created_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)

        if not member.bot:
            whois.add_field(name='Total Messages', value=f"""**{tmsgcount}** messages""", inline=False)
            whois.add_field(name='Total VC Time', value=f"""**{tuserhours}** hours and **{tusermins}** minutes""", inline=False)
            whois.add_field(name='Total Balance', value=f"""**${bal}**""", inline=False)
            whois.add_field(name='Account Type', value=f"""user""", inline=False)
            whois.add_field(name='Highest Role', value=f"""{member.top_role.mention}""", inline=False)
        else:
            whois.add_field(name='Account Type', value=f"""bot""", inline=False)

        whois.add_field(name='Join Position', value=posreal)
        await ctx.send(content=None, embed=whois)

    ##---------- serverinfo -----------##
    @commands.guild_only()
    @commands.command(aliases=['sf'])
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
        whois.add_field(name='Region', value=guild.region, inline=False)

        whois.add_field(name='Stats', value=f"**Members:** {guild.member_count}\n**Categories:** {len(guild.categories)}\n**Text Channels:** {len(guild.text_channels)}\n**Voice Channels:** {len(guild.voice_channels)}\n**Roles:** {len(guild.roles)}\n**Emojis:** {len(guild.emojis)}", inline=False)

        whois.add_field(name='Nitro Server Boosts', value=f"**Tier:** {guild.premium_tier}\n**Boosters:** {guild.premium_subscription_count}", inline=False)

        await ctx.send(content=None, embed=whois)

    ##---------- NITROBOOST -----------##
    @commands.guild_only()
    @commands.command()
    async def boosts(self, ctx):
        members = []
        for member in ctx.author.guild.premium_subscribers:
            members.append(f'<@{member.id}>')
            members = [str(members).replace('[','').replace(']','').replace("'",'').replace("'",'')]
        members = str(members).replace('[','').replace(']','').replace("'",'').replace("'",'')
        nitro = discord.Embed(title='', description=f"""**Tier:** level {ctx.author.guild.premium_tier} \n**Boosts:** {ctx.author.guild.premium_subscription_count} \n**Boosters:** {members}""", color=16580705)

        nitro.set_author(name=f"{ctx.guild.name}'s Nitro Boost Status", icon_url=ctx.guild.icon.url)
        nitro.set_thumbnail(url='https://cdn.discordapp.com/emojis/689542582987915438.gif?v=1')
        await ctx.send(content=None, embed=nitro)

    ##---------- GUILDS -----------##
    @commands.guild_only()
    @commands.command()
    async def guilds(self, ctx):
        guilds = len(self.bot.guilds)
        embed = lib.embed.systemEmbed(f"""Currently in **{guilds}** servers.""", self.bot)
        await ctx.send(content=None, embed=embed)

    ##---------- GUILDS INFO -----------##
    @commands.guild_only()
    @commands.is_owner()
    @commands.command()
    async def guildinfo(self, ctx):
        guilds = len(self.bot.guilds)
        embed = lib.embed.systemEmbed(f"""Currently in **{guilds}** servers.""")
        for server in self.bot.guilds:
            embed.add_field(name=server.name, value=f'**Owner:** {server.owner} **Members:** {server.member_count} **id:** {server.id}', inline=False)
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(InfoCog(bot))