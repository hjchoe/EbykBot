import discord
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import lib.embed
import lib.sql

class LeaderboardsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    ##---------- Message Count ----------##
    @app_commands.command(name="messages", description="Shows the messages of a user.")
    @app_commands.describe(user="The user you want the message info of (enter nothing for your messages).")
    async def messages(self, interaction: discord.Interaction, user: discord.Member=None):
        if user == None:
            userid = interaction.user.id
        else:
            userid = user.id
        umsgcount, tmsgcount, dmsgcount = lib.sql.messagecount(userid, interaction.guild.id)

        embed = await lib.embed.messageEmbed(interaction, userid, umsgcount, tmsgcount, dmsgcount)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Message Leaderboard ----------##
    @app_commands.command(name="message leaderboard", description="Shows the message leaderboard for daily, weekly, or total periods.")
    @app_commands.describe(period="which leaderboard period (daily, weekly, or total).")
    @app_commands.choices(section=[
        Choice(name="Daily", value=0),
        Choice(name="Weekly", value=1),
        Choice(name="Total", value=2),
        Choice(name="All", value=3)
    ])
    async def messageleaderboard(self, interaction: discord.Interaction, period: int):
        if period == 0:
            lb = await lib.sql.dmessageleaderboard(self.bot, interaction.guild.id)
            embed = lib.embed.lbEmbed(interaction, "Daily", lb)
        elif period == 1:
            lb = await lib.sql.messageleaderboard(self.bot, interaction.guild.id)
            embed = lib.embed.lbEmbed(interaction, "Weekly", lb)
        elif period == 2:
            lb = await lib.sql.tmessageleaderboard(self.bot, interaction.guild.id)
            embed = lib.embed.lbEmbed(interaction, "Total", lb)
        elif period == 3:
            lbdaily = await lib.sql.dmessageleaderboard(self.bot, interaction.guild.id)
            embeddaily = lib.embed.lbEmbed(interaction, "Daily", lbdaily)
            lbweekly = await lib.sql.messageleaderboard(self.bot, interaction.guild.id)
            embedweekly = lib.embed.lbEmbed(interaction, "Weekly", lbweekly)
            lbtotal = await lib.sql.tmessageleaderboard(self.bot, interaction.guild.id)
            embedtotal = lib.embed.lbEmbed(interaction, "Total", lbtotal)
            embed = [embeddaily, embedweekly, embedtotal]
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Vc Time ----------##
    @app_commands.command(name="vc", description="Shows the vc time of a user.")
    @app_commands.describe(user="The user you want the vc time info of (enter nothing for your vc time).")
    async def vctime(self, interaction: discord.Interaction, user: discord.Member=None):
        if user == None:
            userid = interaction.author.id
        else:
            userid = user.id
        hours, minutes, thours, tminutes = lib.sql.vcount(userid, interaction.guild.id)
        embed = await lib.embed.vcEmbed(interaction, userid, hours, minutes, thours, tminutes)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Vc Time Leaderboard ----------##
    @app_commands.command(name="vc leaderboard", description="Shows the vc time leaderboard for daily, weekly, or total periods.")
    @app_commands.describe(period="which leaderboard period (daily, weekly, or total).")
    @app_commands.choices(section=[
        Choice(name="Daily", value=0),
        Choice(name="Weekly", value=1),
        Choice(name="Total", value=2),
        Choice(name="All", value=3)
    ])
    async def vcleaderboard(self, interaction: discord.Interaction, period: int):
        if period == 0:
            lb = await lib.sql.dvcleaderboard(self.bot, interaction.guild.id)
            embed = lib.embed.lbEmbed(interaction, "Daily", lb)
        elif period == 1:
            lb = await lib.sql.vcleaderboard(self.bot, interaction.guild.id)
            embed = lib.embed.lbEmbed(interaction, "Weekly", lb)
        elif period == 2:
            lb = await lib.sql.tvcleaderboard(self.bot, interaction.guild.id)
            embed = lib.embed.lbEmbed(interaction, "Total", lb)
        elif period == 3:
            lbdaily = await lib.sql.dvcleaderboard(self.bot, interaction.guild.id)
            embeddaily = lib.embed.lbEmbed(interaction, "Daily", lbdaily)
            lbweekly = await lib.sql.vcleaderboard(self.bot, interaction.guild.id)
            embedweekly = lib.embed.lbEmbed(interaction, "Weekly", lbweekly)
            lbtotal = await lib.sql.tvcleaderboard(self.bot, interaction.guild.id)
            embedtotal = lib.embed.lbEmbed(interaction, "Total", lbtotal)
            embed = [embeddaily, embedweekly, embedtotal]
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Guild Message Count ----------##
    @app_commands.command(name="guild messages", description="Shows the messages of a guild.")
    async def guildmessages(self, interaction = discord.Interaction):
        umsgcount, tmsgcount, dmsgcount = lib.sql.glb_messagecount(interaction.guild.id)
        embed = lib.embed.glb_messageEmbed(interaction, self.bot, umsgcount, tmsgcount, dmsgcount)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Guild Message Leaderboard ----------##
    @slash_util.slash_command(description="Shows the weekly guild message leaderboard.")
    async def guildweeklymessageleaderboard(self, ctx):
        lb = await lib.sql.glb_messageleaderboard(self.bot)
        embed = lib.embed.glb_lbEmbed(ctx, "Weekly", lb)
        await ctx.send(content=None, embed=embed)
    
    ##---------- Guild Total Message Leaderboard ----------##
    @slash_util.slash_command(description="Shows the total guild message leaderboard.")
    async def guildtotalmessageleaderboard(self, ctx):
        lb = await lib.sql.glb_tmessageleaderboard(self.bot)
        embed = lib.embed.glb_lbEmbed(ctx, "Total", lb)
        await ctx.send(content=None, embed=embed)
    
    ##---------- Guild Daily Message Leaderboard ----------##
    @slash_util.slash_command(description="Shows the daily guild message leaderboard.")
    async def guilddailymessageleaderboard(self, ctx):
        lb = await lib.sql.glb_dmessageleaderboard(self.bot)
        embed = lib.embed.glb_lbEmbed(ctx, "Daily", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- Guild Vc Time ----------##
    @slash_util.slash_command(description="Shows the vc time of a guild.")
    async def guildvctime(self, ctx):
        hours, minutes, thours, tminutes = lib.sql.glb_vcount(ctx.guild.id)
        embed = lib.embed.glb_vcEmbed(ctx, self.bot, hours, minutes, thours, tminutes)
        await ctx.send(content=None, embed=embed)

    ##---------- Guild Vc Time Leaderboard ----------##
    @slash_util.slash_command(description="Shows the weekly guild vc time leaderboard.")
    async def guildweeklyvcleaderboard(self, ctx):
        lb = await lib.sql.glb_vcleaderboard(self.bot)
        embed = lib.embed.glb_lbEmbed(ctx, "Weekly", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- Total Vc Time Leaderboard ----------##
    @slash_util.slash_command(description="Shows the total guild vc time leaderboard.")
    async def guildtotalvcleaderboard(self, ctx):
        lb = await lib.sql.glb_tvcleaderboard(self.bot)
        embed = lib.embed.glb_lbEmbed(ctx, "Total", lb)
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(LeaderboardsCog(bot))