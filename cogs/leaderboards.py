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
    @app_commands.command(name="message leaderboard", description="Shows the message leaderboard for daily, weekly, or total periods.")
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
    @app_commands.command(name="vc leaderboard", description="Shows the vc time leaderboard for daily, weekly, or total periods.")
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
    @app_commands.command(name="guild messages", description="Shows the messages of a guild.")
    async def guildmessages(self, interaction = discord.Interaction) -> None:
        umsgcount, tmsgcount, dmsgcount = lib.sql.glb_messagecount(interaction.guild.id)
        embed = lib.embed.glb_messageEmbed(interaction, self.bot, umsgcount, tmsgcount, dmsgcount)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Guild Message Leaderboard ----------##
    @app_commands.command(name="guild message leaderboard", description="Shows the guild message leaderboard for daily, weekly, or total periods.")
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
    @app_commands.command(name="guild vc", description="Shows the vc time of a guild.")
    async def guildvctime(self, interaction: discord.Interaction) -> None:
        hours, minutes, thours, tminutes, dhours, dminutes = lib.sql.glb_vcount(interaction.guild.id)
        embed = lib.embed.glb_vcEmbed(interaction, self.bot, hours, minutes, thours, tminutes, dhours, dminutes)
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Guild Vc Time Leaderboard ----------##
    @app_commands.command(name="guild vc leaderboard", description="Shows the guild vc time leaderboard for daily, weekly, or total periods.")
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

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        #await self.bot.process_commands(message)
        ctx = await self.bot.get_context(message)
        if not ctx.valid:
            if message.author.bot:
                return

            if self.bot.user.mentioned_in(message) and not message.mention_everyone:
                embed = lib.embed.systemEmbed("**prefix:** /\nSend `/help` for my help menu!", self.bot)
                await message.channel.send(content=None, embed=embed)

            if message.guild is None and message.author is not self.bot.user and '/help' not in message.content.lower():
                await message.author.send("Hey I'm Ebyk Bot, run the command **/help** to check out what I offer!")
                return

            conn, c = lib.sql.connect(message.guild.id)
            gconn, gc = lib.sql.glb_connect()

            c.execute("SELECT msgs FROM msgCount WHERE userid = ?", (message.author.id,))
            count = c.fetchone()
            c.execute("SELECT tmsgs FROM totalmsgCount WHERE userid = ?", (message.author.id,))
            tcount = c.fetchone()
            c.execute("SELECT dmsgs FROM dmsgCount WHERE userid = ?", (message.author.id,))
            dcount = c.fetchone()

            gc.execute("SELECT msgs FROM guildmsgcount WHERE guildid = ?", (message.guild.id,))
            gcount = gc.fetchone()
            gc.execute("SELECT tmsgs FROM tguildmsgcount WHERE guildid = ?", (message.guild.id,))
            gtcount = gc.fetchone()
            gc.execute("SELECT dmsgs FROM dguildmsgcount WHERE guildid = ?", (message.guild.id,))
            gdcount = gc.fetchone()

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

            if gcount is None:
                gc.execute('INSERT INTO guildmsgcount (guildid, msgs) VALUES (?,?)', (message.guild.id, 1))
                gconn.commit()
            else:
                oldNum = count[0]
                newNum = oldNum + 1
                gc.execute('UPDATE guildmsgcount SET msgs = ? WHERE guildid = ?', (newNum, message.guild.id))
                gconn.commit()

            if gtcount is None:
                gc.execute('INSERT INTO tguildmsgcount (guildid, tmsgs) VALUES (?,?)', (message.guild.id, 1))
                gconn.commit()
            else:
                toldNum = tcount[0]
                tnewNum = toldNum + 1
                gc.execute('UPDATE tguildmsgcount SET tmsgs = ? WHERE guildid = ?', (tnewNum, message.guild.id))
                gconn.commit()

            if gdcount is None:
                gc.execute('INSERT INTO dguildmsgcount (guildid, dmsgs) VALUES (?,?)', (message.guild.id, 1))
                gconn.commit()
            else:
                doldNum = dcount[0]
                dnewNum = doldNum + 1
                gc.execute('UPDATE dguildmsgcount SET dmsgs = ? WHERE guildid = ?', (dnewNum, message.guild.id))
                gconn.commit()

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
    async def on_voice_state_update(self, member, before, after) -> None:
        if member.bot:
            return

        conn, c = lib.sql.connect(member.guild.id)
        gconn, gc = lib.sql.glb_connect()
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

            c.execute('SELECT vc FROM vcTime WHERE userid = ?', (member.id,))
            vcount = c.fetchone()
            c.execute('SELECT "tvc" FROM "totalvcTime" WHERE "userid" = ?', (member.id,))
            tvcount = c.fetchone()
            c.execute('SELECT dvc FROM dvcTime WHERE userid = ?', (member.id,))
            dvcount = c.fetchone()

            gc.execute('SELECT vc FROM guildvctime WHERE guildid = ?', (member.guild.id,))
            gvcount = gc.fetchone()
            gc.execute('SELECT "tvc" FROM tguildvctime WHERE guildid = ?', (member.guild.id,))
            gtvcount = gc.fetchone()
            gc.execute('SELECT dvc FROM dguildvctime WHERE guildid = ?', (member.guild.id,))
            gdvcount = gc.fetchone()

            if not "day" in str(totalTime):  # checking if date is same
                try:
                    totalMins = int(str(totalTime)[3:5]) + (int(str(totalTime)[0:2]) * 60)
                except:
                    totalMins = int(str(totalTime)[2:4]) + (int(str(totalTime)[0:1]) * 60)
            else:
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

            if tvcount is None:
                c.execute('INSERT INTO "totalvcTime" ("userid", "tvc") VALUES (?,?)', (member.id, totalMins))
                conn.commit()
            else:
                newcount = totalMins + tvcount[0]
                c.execute('UPDATE "totalvcTime" SET "tvc" = ? WHERE  "userid" = ?', (newcount, member.id))
                conn.commit()

            if dvcount is None:
                c.execute('INSERT INTO dvcTime (userid, dvc) VALUES (?,?)', (member.id, totalMins))
                conn.commit()
            else:
                newcount = totalMins + dvcount[0]
                c.execute('UPDATE dvcTime SET dvc = ? WHERE  userid = ?', (newcount, member.id))
                conn.commit()

            if gvcount is None:
                gc.execute('INSERT INTO guildvctime (guildid, vc) VALUES (?,?)', (member.guild.id, totalMins))
                gconn.commit()
            else:
                newcount = totalMins + vcount[0]
                gc.execute('UPDATE guildvctime SET vc = ? WHERE guildid = ?', (newcount, member.guild.id))
                gconn.commit()

            if gtvcount is None:
                gc.execute('INSERT INTO tguildvctime (guildid, tvc) VALUES (?,?)', (member.guild.id, totalMins))
                gconn.commit()
            else:
                newcount = totalMins + tvcount[0]
                gc.execute('UPDATE tguildvctime SET tvc = ? WHERE  guildid = ?', (newcount, member.guild.id))
                gconn.commit()

            if gdvcount is None:
                gc.execute('INSERT INTO dguildvctime (guildid, dvc) VALUES (?,?)', (member.guild.id, totalMins))
                gconn.commit()
            else:
                newcount = totalMins + tvcount[0]
                gc.execute('UPDATE dguildvctime SET dvc = ? WHERE  guildid = ?', (newcount, member.guild.id))
                gconn.commit()        

            c.execute('DELETE FROM timeLog WHERE userid = ?', (member.id,))
            conn.commit()

def setup(bot: commands.Bot):
    bot.add_cog(LeaderboardsCog(bot))