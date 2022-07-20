import discord
from discord.ext import commands
import lib.embed
import lib.sql
import lib.economy

class EconCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##---------- coinflip ----------##
    @commands.guild_only()
    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx, side, betamount):
        bank = lib.sql.balancegrab(ctx.author.id, ctx.guild.id)
        wagerstatus, betamount = lib.economy.checkwager(betamount, bank)
        if wagerstatus == True:
            playstatus, bank = lib.economy.checkbal(bank)
            if playstatus == True:
                sidestatus = lib.economy.checkside(side)
                if sidestatus == True:
                    coin = lib.economy.flipcoin()
                    win = lib.economy.checkwin(side, coin)
                    bank = lib.economy.transaction(ctx.author.id, ctx.guild.id, win, betamount, bank)
                    embed = lib.embed.coinflipEmbed(ctx, ctx.author.id, win, side, coin, betamount, bank)
                elif sidestatus == False:
                    embed = lib.embed.errorEmbed(ctx, f"You have entered an invalid side of the coin. Choose heads or tails.", "Invalid Input Error")
            elif playstatus == False:
                embed = lib.embed.errorEmbed(ctx, f"You do not have enough funds to play. Balance: **${bank}**", "Balance Error")
        elif wagerstatus == False:
            embed = lib.embed.errorEmbed(ctx, f"You can't bet more than you have. Balance: **${bank}**", "Wager Error")
        else:
            embed = lib.embed.errorEmbed(ctx, "Enter a proper integer to bet.", "Invalid Betting Amount Error")
        await ctx.send(content=None, embed=embed)

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = lib.embed.errorEmbed(ctx, "Please use the command properly: `.cf coinside betamount`", "Invalid Command Error")
            await ctx.send(content=None, embed=embed)

    ##---------- Balance Check ----------##
    @commands.guild_only()
    @commands.command(aliases=['bal', 'b'])
    async def balance(self, ctx, member : discord.Member=None):
        if member == None:
            userid = ctx.author.id
        else:
            userid = member.id
        moneyamt = lib.sql.balancegrab(userid, ctx.guild.id)

        embed = await lib.embed.balEmbed(ctx, userid, moneyamt)
        await ctx.send(content=None, embed=embed)

    ##---------- Balance Leaderboard ----------##
    @commands.guild_only()
    @commands.command(aliases=['bleaderboard'])
    async def blb(self, ctx):
        lb = lib.sql.balleaderboard(ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Bank", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- give ----------##
    @commands.guild_only()
    @commands.command(aliases=['g'])
    async def give(self, ctx, member : discord.Member, amount):
        bank = lib.sql.balancegrab(ctx.author.id, ctx.guild.id)
        amountstatus, amount = lib.economy.checkgiveamt(amount, bank)
        if member:
            if amountstatus == True:
                lib.economy.givetransaction(ctx.author.id, member.id, ctx.guild.id, amount)
                embed = lib.embed.giveEmbed(ctx, ctx.author.id, member.id, amount)
            elif amountstatus == False:
                embed = lib.embed.errorEmbed(ctx, f"You can't give more than you have. Balance: **${bank}**", "Balance Error")
            else:
                embed = lib.embed.errorEmbed(ctx, f"Provide a proper integer amount to give somebody", "Invalid Input Error")
        else:
            embed = lib.embed.errorEmbed(ctx, f"Provide a proper user to give money to", "Invalid Input Error")
        await ctx.send(content=None, embed=embed)

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = lib.embed.errorEmbed(ctx, "Please use the command properly: `.give @user amount`", "Invalid Command Error")
            await ctx.send(content=None, embed=embed)
        if isinstance(error, discord.ext.commands.BadArgument):
            embed = lib.embed.errorEmbed(ctx, "Provide a proper user to give money to", "Invalid Input Error")
            await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(EconCog(bot))