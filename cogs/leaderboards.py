import discord
from discord.ext import commands
import datetime
import lib.embed
import lib.sql

class LeaderboardsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##---------- Message Count ----------##
    @commands.guild_only()
    @commands.command(aliases=['msg', 'messages'])
    async def m(self, ctx, member : discord.Member=None):
        if member == None:
            userid = ctx.author.id
        else:
            userid = member.id
        umsgcount, tmsgcount, dmsgcount = lib.sql.messagecount(userid, ctx.guild.id)

        embed = lib.embed.messageEmbed(ctx, userid, umsgcount, tmsgcount, dmsgcount)
        await ctx.send(content=None, embed=embed)

    ##---------- Message Leaderboard ----------##
    @commands.guild_only()
    @commands.command(aliases=['mleaderboard'])
    async def mlb(self, ctx):
        lb = lib.sql.messageleaderboard(ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Weekly", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- Total Message Leaderboard ----------##
    @commands.guild_only()
    @commands.command(aliases=['tmleaderboard'])
    async def tmlb(self, ctx):
        lb = lib.sql.tmessageleaderboard(ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Total", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- Daily Message Leaderboard ----------##
    @commands.guild_only()
    @commands.command(aliases=['dmleaderboard'])
    async def dmlb(self, ctx):
        lb = lib.sql.dmessageleaderboard(ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Daily", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- Vc Time ----------##
    @commands.guild_only()
    @commands.command()
    async def vc(self, ctx, member : discord.Member=None):
        if member == None:
            userid = ctx.author.id
        else:
            userid = member.id
        hours, minutes, thours, tminutes = lib.sql.vcount(userid, ctx.guild.id)
        embed = lib.embed.vcEmbed(ctx, userid, hours, minutes, thours, tminutes)
        await ctx.send(content=None, embed=embed)

    ##---------- Vc Time Leaderboard ----------##
    @commands.guild_only()
    @commands.command()
    async def vclb(self, ctx):
        lb = lib.sql.vcleaderboard(ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Weekly", lb)
        await ctx.send(content=None, embed=embed)

    ##---------- Total Vc Time Leaderboard ----------##
    @commands.guild_only()
    @commands.command()
    async def tvclb(self, ctx):
        lb = lib.sql.tvcleaderboard(ctx.guild.id)
        embed = lib.embed.lbEmbed(ctx, "Total", lb)
        await ctx.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        #await self.bot.process_commands(message)
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            pass
        else:
            if message.author.bot:
                return

            if self.bot.user.mentioned_in(message) and not message.mention_everyone:
                embed = lib.embed.systemEmbed("**prefix:** eb ___\nSend `eb help` for my help menu!", self.bot)
                await message.channel.send(content=None, embed=embed)

            if message.guild is None and message.author is not self.bot.user and not 'eb help' in message.content.lower():
                await message.author.send("Hey I'm Ebyk Bot, run the command **eb help** to check out what I offer!")
                return

            conn, c = lib.sql.connect(message.guild.id)

            c.execute("SELECT msgs FROM msgCount WHERE userid = ?", (message.author.id,))
            count = c.fetchone()
            c.execute("SELECT tmsgs FROM totalmsgCount WHERE userid = ?", (message.author.id,))
            tcount = c.fetchone()
            c.execute("SELECT dmsgs FROM dmsgCount WHERE userid = ?", (message.author.id,))
            dcount = c.fetchone()

            if count is None:
                c.execute('INSERT INTO msgCount (userid, msgs) VALUES (?,?)', (message.author.id, 1))
                conn.commit()
            else:
                oldNum = count[0]
                newNum = oldNum + 1
                c.execute('UPDATE msgCount SET msgs = ? WHERE userid = ?', (newNum, message.author.id))
                conn.commit()

            if tcount is None:
                c.execute('INSERT INTO totalmsgCount (userid, tmsgs) VALUES (?,?)', (message.author.id, 1))
                conn.commit()
            else:
                toldNum = tcount[0]
                tnewNum = toldNum + 1
                c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (tnewNum, message.author.id))
                conn.commit()

            if dcount is None:
                c.execute('INSERT INTO dmsgCount (userid, dmsgs) VALUES (?,?)', (message.author.id, 1))
                conn.commit()
            else:
                doldNum = dcount[0]
                dnewNum = doldNum + 1
                c.execute('UPDATE dmsgCount SET dmsgs = ? WHERE userid = ?', (dnewNum, message.author.id))
                conn.commit()

            c.execute("SELECT money FROM bank WHERE userid = ?", (message.author.id,))
            kaching = c.fetchone()

            if kaching is None:
                c.execute('INSERT INTO bank (userid, money) VALUES (?,?)', (message.author.id, 1))
                conn.commit()
            else:
                oldNum = kaching[0]
                newNum = oldNum + 1
                c.execute('UPDATE bank SET money = ? WHERE userid = ?', (newNum, message.author.id))
                conn.commit()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        conn, c = lib.sql.connect(member.guild.id)
        if before.channel is None and not after.channel is None and not after.afk: #vc join
            timestart = datetime.datetime.utcnow()
            c.execute('INSERT INTO timeLog (userid, jTime) VALUES (?,?)', (member.id, timestart))
            conn.commit()

        if before.afk and not after.channel is None: #moving from afk to channel
            timestart = datetime.datetime.utcnow()
            c.execute('INSERT INTO timeLog (userid, jTime) VALUES (?,?)', (member.id, timestart))
            conn.commit()

        if after.channel == None or after.afk: #vc left

            c.execute('SELECT jTime FROM timeLog WHERE userid = ?', (member.id,))
            jTimeList = c.fetchone()
            jTime = jTimeList[0]
            lTime = datetime.datetime.utcnow()
            sjTime = str(jTime)
            slTime = str(lTime)
            jTimeHours = int(sjTime[11:13])
            lTimeHours = int(slTime[11:13])
            jTimeMins = int(sjTime[14:16])
            lTimeMins = int(sjTime[14:16])
            jTimeDay = int(sjTime[8:10])
            jTimeMonth = int(sjTime[5:7])
            jTimeYear = int(sjTime[0:4])
            fjTime = datetime.datetime(jTimeYear, jTimeMonth, jTimeDay, jTimeHours, jTimeMins)
            totalTime = lTime - fjTime

            if not "day" in str(totalTime):  # checking if date is same
                c.execute('SELECT vc FROM vcTime WHERE userid = ?', (member.id,))
                vcount = c.fetchone()
                c.execute('SELECT "tvc" FROM "totalvcTime" WHERE "userid" = ?', (member.id,))
                tvcount = c.fetchone()

                try:
                    totalMins = int(str(totalTime)[3:5]) + (int(str(totalTime)[0:2]) * 60)
                except:
                    totalMins = int(str(totalTime)[2:4]) + (int(str(totalTime)[0:1]) * 60)

                if vcount is None:
                    c.execute('INSERT INTO vcTime (userid, vc) VALUES (?,?)', (member.id, totalMins))
                    conn.commit()
                else:
                    newcount = totalMins + vcount[0]
                    c.execute('UPDATE vcTime SET vc = ? WHERE userid = ?', (newcount, member.id))
                    conn.commit()

                if tvcount is None:
                    c.execute('INSERT INTO "totalvcTime" ("userid", "tvc") VALUES (?,?)', (member.id, totalMins))
                    conn.commit()
                    c.execute('DELETE FROM timeLog WHERE userid = ?', (member.id,))
                    conn.commit()
                else:
                    newcount = totalMins + tvcount[0]
                    c.execute('UPDATE "totalvcTime" SET "tvc" = ? WHERE  "userid" = ?', (newcount, member.id))
                    conn.commit()
                    c.execute('DELETE FROM timeLog WHERE userid = ?', (member.id,))
                    conn.commit()
            else:
                c.execute('SELECT vc FROM vcTime WHERE userid = ?', (member.id,))
                vcount = c.fetchone()
                c.execute('SELECT "tvc" FROM "totalvcTime" WHERE "userid" = ?', (member.id,))
                tvcount = c.fetchone()

                try:
                    totalMins = ((int(str(totalTime)[0]) * 24) * 60) + int(str(totalTime)[10:12]) + (int(str(totalTime)[7:9]) * 60)
                except:
                    totalMins = ((int(str(totalTime)[0]) * 24) * 60) + int(str(totalTime)[9:11]) + (int(str(totalTime)[7:8]) * 60)

                if vcount is None:
                    c.execute('INSERT INTO vcTime (userid, vc) VALUES (?,?)', (member.id, totalMins))
                    conn.commit()
                else:
                    newcount = totalMins + vcount[0]
                    c.execute('UPDATE vcTime SET vc = ? WHERE userid = ?', (newcount, member.id))
                    conn.commit()
                    c.execute('DELETE FROM timeLog WHERE userid = ?', (member.id,))
                    conn.commit()

                if tvcount is None:
                    c.execute('INSERT INTO "totalvcTime" ("userid", "tvc") VALUES (?,?)', (member.id, totalMins))
                    conn.commit()
                else:
                    newcount = totalMins + tvcount[0]
                    c.execute('UPDATE "totalvcTime" SET "tvc" = ? WHERE  "userid" = ?', (newcount, member.id))
                    conn.commit()
                    c.execute('DELETE FROM timeLog WHERE userid = ?', (member.id,))
                    conn.commit()

def setup(bot):
    bot.add_cog(LeaderboardsCog(bot))