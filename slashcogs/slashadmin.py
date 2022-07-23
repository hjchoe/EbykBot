import discord
from discord.ext import commands
import lib.slash_util as slash_util
import lib.embed
import lib.sql
import lib.economy

class sAdminCog(slash_util.ApplicationCog):
    ##---------- Admin Total Message LB Reset -----------##
    @slash_util.slash_command(description="[ADMIN] Reset total message leaderboard.")
    async def reset_total_mlb(self, ctx):
        if (ctx.author.guild_permissions.administrator):
            lib.sql.resettmlb(ctx.guild.id)
            embed = lib.embed.systemEmbed("Finished manual reset of total message leaderboard", self.bot)
            await ctx.send(content=None, embed=embed)
        else:
            embed = lib.embed.errorEmbed(ctx, "Failed to reset total message leaderboard", "Missing Admin Permissions")
            await ctx.send(content=None, embed=embed)

    ##---------- Admin Total Voice LB Reset -----------##
    @slash_util.slash_command(description="[ADMIN] Reset total voice leaderboard.")
    async def reset_total_vclb(self, ctx):
        if (ctx.author.guild_permissions.administrator):
            lib.sql.resettvclb(ctx.guild.id)
            embed = lib.embed.systemEmbed("Finished manual reset of total voice leaderboard", self.bot)
            await ctx.send(content=None, embed=embed)
        else:
            embed = lib.embed.errorEmbed(ctx, "Failed to reset total voice leaderboard", "Missing Admin Permissions")
            await ctx.send(content=None, embed=embed)
            
    ##---------- Admin Message Remove -----------##
    @slash_util.slash_command(description="[ADMIN] Remove a certain amount of messages from a user.")
    @slash_util.describe(user="The user you want to remove messages from.")
    @slash_util.describe(messages="The number of messages to remove.")
    async def removemessages(self, ctx, user: discord.Member, messages: int):
        if (ctx.author.guild_permissions.administrator):
            conn, c = lib.sql.connect(ctx.guild.id)
            c.execute("SELECT tmsgs from totalmsgCount WHERE userid = ?", (user.id,))
            tcount = c.fetchone()
            if int(messages) > int(tcount[0]):
                newtcount = 0
                c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (newtcount, user.id))
                conn.commit()
            else:
                newtcount = int(tcount[0])-int(messages)
                c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (newtcount, user.id))
                conn.commit()

            embed = lib.embed.systemEmbed(f"Removed {messages} messages from {user.mention}. They are now at {newtcount} messages.", self.bot)
            await ctx.send(content=None, embed=embed)
        else:
            embed = lib.embed.errorEmbed(ctx, f"Failed to remove {messages} messages from {user.mention}", "Missing Admin Permissions")
            await ctx.send(content=None, embed=embed)

    ##---------- Set Invite Code -----------##
    @slash_util.slash_command(description="[ADMIN] Set the invite code for your server to show up in guild leaderboards.")
    @slash_util.describe(code="The invite code you want to set for your server.")
    async def invitecode(self, ctx, code: str):
        conn, c = lib.sql.glb_connect()

        c.execute("SELECT code from invitecode WHERE guildid = ?", (ctx.guild.id,))
        invcode = c.fetchone()

        code = code.replace("https://discord.gg/",'')

        if invcode is None:
            c.execute('INSERT INTO invitecode (guildid, code) VALUES (?,?)', (ctx.guild.id, code))
            conn.commit()
        else:
            c.execute('UPDATE invitecode SET code = ? WHERE guildid = ?', (code, ctx.guild.id))
            conn.commit()

        embed = lib.embed.systemEmbed(f"Set {ctx.guild.name}'s invite to: https://discord.gg/{code}.", self.bot)
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(sAdminCog(bot))