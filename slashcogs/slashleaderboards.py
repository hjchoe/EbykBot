import discord
import lib.slash_util as slash_util
import lib.embed
import lib.sql

class sLeaderboardsCog(slash_util.ApplicationCog):
    ##---------- Message Count ----------##
    @slash_util.slash_command(description="Shows the messages of a user.")
    @slash_util.describe(user="The user you want the message info of.")
    async def messages(self, ctx, user: discord.Member=None):
        if user == None:
            userid = ctx.author.id
        else:
            userid = user.id
        umsgcount, tmsgcount, dmsgcount = lib.sql.messagecount(userid, ctx.guild.id)

        embed = await lib.embed.messageEmbed(ctx, userid, umsgcount, tmsgcount, dmsgcount)
        await ctx.send(content=None, embed=embed)

    ##---------- Message Leaderboard ----------##
    @slash_util.slash_command(description="Shows the weekly message leaderboard.")
    async def weeklymessageleaderboard(self, ctx):
        lb = await lib.sql.messageleaderboard(self.bot, ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Weekly", lb)
        await ctx.send(content=None, embed=embed)
    
    ##---------- Total Message Leaderboard ----------##
    @slash_util.slash_command(description="Shows the total message leaderboard.")
    async def totalmessageleaderboard(self, ctx):
        lb = await lib.sql.tmessageleaderboard(self.bot, ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Total", lb)
        await ctx.send(content=None, embed=embed)
    
    ##---------- Daily Message Leaderboard ----------##
    @slash_util.slash_command(description="Shows the daily message leaderboard.")
    async def dailymessageleaderboard(self, ctx):
        lb = await lib.sql.dmessageleaderboard(self.bot, ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Daily", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- Vc Time ----------##
    @slash_util.slash_command(description="Shows the vc time of a user.")
    @slash_util.describe(user="The user you want the vc time info of.")
    async def vctime(self, ctx, user: discord.Member=None):
        if user == None:
            userid = ctx.author.id
        else:
            userid = user.id
        hours, minutes, thours, tminutes = lib.sql.vcount(userid, ctx.guild.id)
        embed = await lib.embed.vcEmbed(ctx, userid, hours, minutes, thours, tminutes)
        await ctx.send(content=None, embed=embed)

    ##---------- Vc Time Leaderboard ----------##
    @slash_util.slash_command(description="Shows the weekly vc time leaderboard.")
    async def weeklyvcleaderboard(self, ctx):
        lb = await lib.sql.vcleaderboard(self.bot, ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Weekly", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- Total Vc Time Leaderboard ----------##
    @slash_util.slash_command(description="Shows the total vc time leaderboard.")
    async def totalvcleaderboard(self, ctx):
        lb = await lib.sql.tvcleaderboard(self.bot, ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Total", lb)
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(sLeaderboardsCog(bot))