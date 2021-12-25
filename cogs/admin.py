import discord
from discord.ext import commands
import lib.embed
import lib.sql

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    ##---------- Admin Total Message LB Reset -----------##
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['rtmlb'])
    async def reset_total_mlb(self, ctx):
        lib.sql.resettmlb(ctx.guild.id)
        embed = lib.embed.systemEmbed("Finished manual reset of total message leaderboard", self.bot)
        await ctx.send(content=None, embed=embed)
        
    @reset_total_mlb.error
    async def reset_total_mlb_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = lib.embed.errorEmbed(ctx, "Failed to reset total message leaderboard", "Missing Admin Permissions")
            await ctx.send(content=None, embed=embed)

    ##---------- Admin Total Voice LB Reset -----------##
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['rtvclb'])
    async def reset_total_vclb(self, ctx):
        lib.sql.resettvclb(ctx.guild.id)
        embed = lib.embed.systemEmbed("Finished manual reset of total voice leaderboard", self.bot)
        await ctx.send(content=None, embed=embed)
        
    @reset_total_vclb.error
    async def reset_total_vclb_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = lib.embed.errorEmbed(ctx, "Failed to reset total voice leaderboard", "Missing Admin Permissions")
            await ctx.send(content=None, embed=embed)
            
    ##---------- Admin Message Remove -----------##
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['rm'])
    async def removemessages(self, ctx, member : discord.Member, messages):
        conn, c = lib.sql.connect(ctx.guild.id)
        c.execute("SELECT tmsgs from totalmsgCount WHERE userid = ?", (member.id,))
        tcount = c.fetchone()
        if int(messages) > int(tcount[0]):
            newtcount = 0
            c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (newtcount, member.id))
            conn.commit()
        else:
            newtcount = int(tcount[0])-int(messages)
            c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (newtcount, member.id))
            conn.commit()

        embed = lib.embed.systemEmbed(f"Removed {messages} messages from {member.mention}. They are now at {newtcount} messages.", self.bot)
        await ctx.send(content=None, embed=embed)

    @removemessages.error
    async def removemessages_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = lib.embed.errorEmbed(ctx, "Failed to remove messages.", "Missing Admin Permissions")
            await ctx.send(content=None, embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = lib.embed.errorEmbed(ctx, "Proper usage is: eb removemessages @user numberofmessages", "Incorrect Syntax")
            await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(AdminCog(bot))