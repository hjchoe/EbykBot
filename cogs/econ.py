import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import lib.embed
import lib.sql
import lib.economy

class EconCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    ##---------- coinflip ----------##
    @app_commands.command(name="coin flip", description="Flip a coin and wager for a 50/50 chance at x2.")
    @app_commands.describe(side="The side of the coin to bet on: 'heads' or 'tails'.", betamount="The amount of money to bet.")
    @app_commands.choices(side=[
        Choice(name="heads", value="heads"),
        Choice(name="tails", value="tails")
    ])
    async def coinflip(self, interaction: discord.Interaction, side: str, betamount: int) -> None:
        bank = lib.sql.balancegrab(interaction.author.id, interaction.guild.id)
        wagerstatus, betamount = lib.economy.checkwager(betamount, bank)
        if wagerstatus == True:
            playstatus, bank = lib.economy.checkbal(bank)
            if playstatus == True:
                coin = lib.economy.flipcoin()
                win = lib.economy.checkwin(side, coin)
                bank = lib.economy.transaction(interaction.author.id, interaction.guild.id, win, betamount, bank)
                embed = lib.embed.coinflipEmbed(interaction, interaction.author.id, win, side, coin, betamount, bank)
            elif playstatus == False:
                embed = lib.embed.errorEmbed(interaction, f"You do not have enough funds to play. Balance: **${bank}**", "Balance Error")
        elif wagerstatus == False:
            embed = lib.embed.errorEmbed(interaction, f"You can't bet more than you have. Balance: **${bank}**", "Wager Error")
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Balance Check ----------##
    @app_commands.command(name="balance", description="Check balance of a user.")
    @app_commands.describe(user="The user you want the balance of (enter nothing for your balance).")
    async def balance(self, interaction: discord.Interaction, user: discord.Member=None) -> None:
        if user == None:
            userid = interaction.author.id
        else:
            userid = user.id
        moneyamt = lib.sql.balancegrab(userid, interaction.guild.id)

        embed = await lib.embed.balEmbed(interaction, userid, moneyamt)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Balance Leaderboard ----------##
    @app_commands.command(name="balance leaderboard", description="Shows balance leaderboard.")
    async def balanceleaderboard(self, interaction: discord.Interaction) -> None:
        lb = await lib.sql.balleaderboard(self.bot, interaction.guild.id)
        embed = lib.embed.lbEmbed(interaction, "Bank", lb)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- give ----------##
    @app_commands.command(description="Give an amount of your money to another user.")
    @app_commands.describe(user="The user you want to transfer your money to.", amount="The amount to transfer.")
    async def give(self, interaction: discord.Interaction, user: discord.Member, amount: int) -> None:
        bank = lib.sql.balancegrab(interaction.author.id, interaction.guild.id)
        amountstatus, amount = lib.economy.checkgiveamt(amount, bank)
        if amountstatus == True:
            lib.economy.givetransaction(interaction.author.id, user.id, interaction.guild.id, amount)
            embed = lib.embed.giveEmbed(interaction, interaction.author.id, user.id, amount)
        elif amountstatus == False:
            embed = lib.embed.errorEmbed(interaction, f"You can't give more than you have. Balance: **${bank}**", "Balance Error")
        await interaction.response.send_message(content=None, embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(EconCog(bot))