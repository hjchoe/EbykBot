##-------------------------------------------------- IMPORTS ---------------------------------------------------##

import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands

import lib.embed
import lib.economy
import lib.sql

import asyncio
import time
import datetime

intents = discord.Intents.default()
intents.messages = True
intents.members = False
intents.presences = False

appid = 800171925275017237
testappid = 809790823780450304

extensions = ['cogs.general', 'cogs.leaderboards', 'cogs.info', 'cogs.econ', 'cogs.admin']
# slashextensions = ['slashcogs.slashgeneral', 'slashcogs.slashleaderboards', 'slashcogs.slashinfo', 'slashcogs.slashecon', 'slashcogs.slashadmin']

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="eb ", case_insensitive=True, owner_id=329326685185114115, help_command=None, tree_cls=app_commands.tree.CommandTree, intents=intents, application_id=testappid)
        #self.setup_hook(self)

    async def setup_hook(self):
        print("loading extensions:")

        await self.load_extension('testcog')
        print("    loaded test cog")

        for ext in extensions:
            try:
                await bot.load_extension(ext)
                print(f"    loaded cog: {ext}")
            except:
                print(f"        FAILED LOADING COG: {ext}")

        await self.sync()
    
    async def sync(self):
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    async def on_connect(self):
        print("Connected!")

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def updatestatus(bot):
        """
        totalusers = 0
        for server in bot.guilds:
            totalusers += len(server.members)
        """
        servercount = len(bot.guilds)
        
        activity = discord.Game(name=f"{servercount} servers | /help")
        await bot.change_presence(status=discord.Status.online, activity=activity)

    async def close(self):
        await super().close()
        await self.session.close()

bot = MyBot()

##-------------------------------------------------- DEFINITIONS ---------------------------------------------------##

tokenpath = "ebykbottoken.txt"
testtokenpath = "ebyktest.txt"

def read_token():
    with open(testtokenpath, "r") as f:
        lines = f.readlines()
        return lines[0].strip()

##-------------------------------------------------- EVENTS ---------------------------------------------------##

@bot.event
async def on_message(self, message) -> None:
    print("detected message")
    await self.bot.process_commands(message)

    if message.author.bot:
        return

    if self.bot.user.mentioned_in(message) and not message.mention_everyone:
        embed = lib.embed.systemEmbed("**prefix:** /\nSend `/help` for my help menu!", self.bot)
        await message.channel.send(content=None, embed=embed)

    if message.guild is None and message.author is not self.bot.user:
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

@bot.event
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

##-------------------------------------------------- Task Loops ---------------------------------------------------##

@tasks.loop(hours=1.0)
async def updatestats():
    await bot.wait_until_ready()
    await bot.updatestatus(bot)

@tasks.loop(hours=12.0)
async def checkday():
    await bot.wait_until_ready()
    day = datetime.datetime.today().strftime('%A')
    if day == "Sunday":
        lib.sql.resetlb()
        lib.sql.cleanTimeLog()

@tasks.loop(hours=24.0)
async def resetdailylb():
    await bot.wait_until_ready()
    lib.sql.resetdlb()

async def main():
    token = read_token()
    lib.sql.cleanTimeLog()
    await bot.start(token)
    await updatestats.start()
    await checkday.start()
    await resetdailylb.start()

asyncio.run(main())
