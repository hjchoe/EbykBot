import discord
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import datetime
import lib.embed
import lib.sql

class LeaderboardsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    ##---------- Message Count ----------##
    @app_commands.command(name="messages", description="Shows the messages of a user.")
    @app_commands.describe(user="The user you want the message info of (enter nothing for your messages).")
    async def messages(self, interaction: discord.Interaction, user: discord.Member=None) -> None:
        if user == None:
            userid = interaction.user.id
        else:
            userid = user.id
        umsgcount, tmsgcount, dmsgcount = lib.sql.messagecount(userid, interaction.guild.id)

        embed = await lib.embed.messageEmbed(interaction, userid, umsgcount, tmsgcount, dmsgcount)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Message Leaderboard ----------##
    @app_commands.command(name="message_leaderboard", description="Shows the message leaderboard for daily, weekly, or total periods.")
    @app_commands.describe(period="which leaderboard period (daily, weekly, or total).")
    @app_commands.choices(period=[
        Choice(name="Daily", value=0),
        Choice(name="Weekly", value=1),
        Choice(name="Total", value=2),
        Choice(name="All", value=3)
    ])
    async def messageleaderboard(self, interaction: discord.Interaction, period: int) -> None:
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
    async def vctime(self, interaction: discord.Interaction, user: discord.Member=None) -> None:
        if user == None:
            userid = interaction.author.id
        else:
            userid = user.id
        hours, minutes, thours, tminutes, dhours, dminutes = lib.sql.vcount(userid, interaction.guild.id)
        embed = await lib.embed.vcEmbed(interaction, userid, hours, minutes, thours, tminutes, dhours, dminutes)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Vc Time Leaderboard ----------##
    @app_commands.command(name="vc_leaderboard", description="Shows the vc time leaderboard for daily, weekly, or total periods.")
    @app_commands.describe(period="which leaderboard period (daily, weekly, or total).")
    @app_commands.choices(period=[
        Choice(name="Daily", value=0),
        Choice(name="Weekly", value=1),
        Choice(name="Total", value=2),
        Choice(name="All", value=3)
    ])
    async def vcleaderboard(self, interaction: discord.Interaction, period: int) -> None:
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
    @app_commands.command(name="guild_messages", description="Shows the messages of a guild.")
    async def guildmessages(self, interaction = discord.Interaction) -> None:
        umsgcount, tmsgcount, dmsgcount = lib.sql.glb_messagecount(interaction.guild.id)
        embed = lib.embed.glb_messageEmbed(interaction, self.bot, umsgcount, tmsgcount, dmsgcount)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Guild Message Leaderboard ----------##
    @app_commands.command(name="guild_message_leaderboard", description="Shows the guild message leaderboard for daily, weekly, or total periods.")
    @app_commands.describe(period="which leaderboard period (daily, weekly, or total).")
    @app_commands.choices(period=[
        Choice(name="Daily", value=0),
        Choice(name="Weekly", value=1),
        Choice(name="Total", value=2),
        Choice(name="All", value=3)
    ])
    async def guildmessageleaderboard(self, interaction: discord.Interaction, period: int) -> None:
        if period == 0:
            lb = await lib.sql.glb_dmessageleaderboard(self.bot)
            embed = lib.embed.glb_lbEmbed(interaction, "Daily", lb)
        elif period == 1:
            lb = await lib.sql.glb_messageleaderboard(self.bot)
            embed = lib.embed.glb_lbEmbed(interaction, "Weekly", lb)
        elif period == 2:
            lb = await lib.sql.glb_tmessageleaderboard(self.bot)
            embed = lib.embed.glb_lbEmbed(interaction, "Total", lb)
        elif period == 3:
            lbdaily = await lib.sql.glb_dmessageleaderboard(self.bot, interaction.guild.id)
            embeddaily = lib.embed.glb_lbEmbed(interaction, "Daily", lbdaily)
            lbweekly = await lib.sql.glb_messageleaderboard(self.bot, interaction.guild.id)
            embedweekly = lib.embed.glb_lbEmbed(interaction, "Weekly", lbweekly)
            lbtotal = await lib.sql.glb_tmessageleaderboard(self.bot, interaction.guild.id)
            embedtotal = lib.embed.glb_lbEmbed(interaction, "Total", lbtotal)
            embed = [embeddaily, embedweekly, embedtotal]
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Guild Vc Time ----------##
    @app_commands.command(name="guild_vc", description="Shows the vc time of a guild.")
    async def guildvctime(self, interaction: discord.Interaction) -> None:
        hours, minutes, thours, tminutes, dhours, dminutes = lib.sql.glb_vcount(interaction.guild.id)
        embed = lib.embed.glb_vcEmbed(interaction, self.bot, hours, minutes, thours, tminutes, dhours, dminutes)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Guild Vc Time Leaderboard ----------##
    @app_commands.command(name="guild_vc_leaderboard", description="Shows the guild vc time leaderboard for daily, weekly, or total periods.")
    @app_commands.describe(period="which leaderboard period (daily, weekly, or total).")
    @app_commands.choices(period=[
        Choice(name="Daily", value=0),
        Choice(name="Weekly", value=1),
        Choice(name="Total", value=2),
        Choice(name="All", value=3)
    ])
    async def guildmessageleaderboard(self, interaction: discord.Interaction, period: int) -> None:
        if period == 0:
            lb = await lib.sql.glb_dmessageleaderboard(self.bot)
            embed = lib.embed.glb_lbEmbed(interaction, "Daily", lb)
        elif period == 1:
            lb = await lib.sql.glb_vcleaderboard(self.bot)
            embed = lib.embed.glb_lbEmbed(interaction, "Weekly", lb)
        elif period == 2:
            lb = await lib.sql.glb_tvcleaderboard(self.bot)
            embed = lib.embed.glb_lbEmbed(interaction, "Total", lb)
        elif period == 3:
            lbdaily = await lib.sql.glb_dvcleaderboard(self.bot, interaction.guild.id)
            embeddaily = lib.embed.glb_lbEmbed(interaction, "Daily", lbdaily)
            lbweekly = await lib.sql.glb_vcleaderboard(self.bot, interaction.guild.id)
            embedweekly = lib.embed.glb_lbEmbed(interaction, "Weekly", lbweekly)
            lbtotal = await lib.sql.glb_tvcleaderboard(self.bot, interaction.guild.id)
            embedtotal = lib.embed.glb_lbEmbed(interaction, "Total", lbtotal)
            embed = [embeddaily, embedweekly, embedtotal]
        await interaction.response.send_message(content=None, embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LeaderboardsCog(bot))