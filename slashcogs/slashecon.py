import discord
import lib.slash_util as slash_util
import lib.embed
import lib.sql
import lib.economy

class sEconCog(slash_util.ApplicationCog):
    ##---------- coinflip ----------##
    @slash_util.slash_command(description="Flip a coin and wager for a 50/50 chance at x2.")
    @slash_util.describe(side="The side of the coin to bet on: 'heads' or 'tails'.")
    @slash_util.describe(betamount="The amount of money to bet.")
    async def coinflip(self, ctx, side: str, betamount: int):
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
        await ctx.send(content=None, embed=embed)

    ##---------- Balance Check ----------##
    @slash_util.slash_command(description="Check balance of a user.")
    @slash_util.describe(user="The user you want the balance of.")
    async def balance(self, ctx, user: discord.Member=None):
        if user == None:
            userid = ctx.author.id
        else:
            userid = user.id
        moneyamt = lib.sql.balancegrab(userid, ctx.guild.id)

        embed = await lib.embed.balEmbed(ctx, userid, moneyamt)
        await ctx.send(content=None, embed=embed)

    ##---------- Balance Leaderboard ----------##
    @slash_util.slash_command(description="Shows balance leaderboard.")
    async def balanceleaderboard(self, ctx):
        lb = lib.sql.balleaderboard(ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Bank", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- give ----------##
    @slash_util.slash_command(description="Give an amount of your money to another user.")
    @slash_util.describe(user="The user you want to transfer your money to.")
    @slash_util.describe(amount="The amount to transfer.")
    async def give(self, ctx, user: discord.Member, amount: int):
        bank = lib.sql.balancegrab(ctx.author.id, ctx.guild.id)
        amountstatus, amount = lib.economy.checkgiveamt(amount, bank)
        if amountstatus == True:
            lib.economy.givetransaction(ctx.author.id, user.id, ctx.guild.id, amount)
            embed = lib.embed.giveEmbed(ctx, ctx.author.id, user.id, amount)
        elif amountstatus == False:
            embed = lib.embed.errorEmbed(ctx, f"You can't give more than you have. Balance: **${bank}**", "Balance Error")
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(sEconCog(bot))