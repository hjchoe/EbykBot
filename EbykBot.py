##-------------------------------------------------- IMPORTS ---------------------------------------------------##

import discord
from discord.ext import tasks
import sqlite3
from discord.ext import commands
import datetime
from datetime import timedelta
import random
import asyncio
import time
import requests
import os
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='eb ', case_insensitive=True, owner_id=329326685185114115, help_command=None, intents=intents)

##-------------------------------------------------- DEFINITIONS ---------------------------------------------------##

def read_token():
    with open("ebykbottoken.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

def resetlb():
    for filename in os.listdir('/home/ebyk/ebykdb'):
        conn = sqlite3.connect(f"/home/ebyk/ebykdb/{filename}")
        c = conn.cursor()
        try:
            c.execute('UPDATE msgCount SET msgs = 0 WHERE msgs < 999999')
            c.execute('UPDATE vcTime SET vc = 0 WHERE vc < 999999')
            conn.commit()
            print(f"Leaderboard Reset Succeeded for {filename}")
        except:
            print(f"Leaderboard Reset Failed for {filename}")

async def updatestatus():
    totalusers = 0
    for server in bot.guilds:
        totalusers += len(server.members)
    activity = discord.Game(name=f"{totalusers} users!")
    await bot.change_presence(status=discord.Status.online, activity=activity)

##---------- SQL CONNECT -----------##
def connect(guildid):
    filename = f"/home/ebyk/ebykdb/({guildid}) sql.db"
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    return conn, c

##---------- FORMAT -----------##
def sqlTOstr(sqlformat):
    replace_str=('(',')',',',"'","'")
    strformat = str(sqlformat)
    for r_str in replace_str:
        strformat = strformat.replace(r_str,'')
    return strformat

##---------- SQL GRAB -----------##
def messagecount(userid, guildid):
    conn, c = connect(guildid)
    try:
        c.execute("SELECT msgs FROM msgCount WHERE userid = ?", (userid,))
        count = c.fetchone()
        c.execute("SELECT tmsgs from totalmsgCount WHERE userid = ?", (userid,))
        tcount = c.fetchone()

        if count is None:
            count = 0
            
        if tcount is None:
            tcount = 0

        umsgcount = sqlTOstr(count)
        tmsgcount = sqlTOstr(tcount)
        return umsgcount, tmsgcount
    except:
        return None

def messageleaderboard(guildid):
    conn, c = connect(guildid)
    try:
        c.execute('SELECT userid FROM msgCount ORDER BY msgs DESC')
        all_user = c.fetchall()
        c.execute('SELECT msgs FROM msgCount ORDER BY msgs DESC')
        all_msgs = c.fetchall()

        if len(all_user) < 10:
            listrange = len(all_user)
        else:
            listrange = 10
        the_list = ''
        for x in range(listrange):
            user = sqlTOstr(all_user[x])
            msgs = sqlTOstr(all_msgs[x])
            try:
                the_list += f'{str(x + 1)}. <@{user}> - **{msgs} messages **\n'
            except:
                pass
        return the_list
    except:
        return None

def tmessageleaderboard(guildid):
    conn, c = connect(guildid)
    try:
        c.execute('SELECT userid FROM totalmsgCount ORDER BY tmsgs DESC')
        all_user = c.fetchall()
        c.execute('SELECT tmsgs FROM totalmsgCount ORDER BY tmsgs DESC')
        all_msgs = c.fetchall()

        if len(all_user) < 10:
            listrange = len(all_user)
        else:
            listrange = 10

        the_list = ''
        for x in range(listrange):
            user = sqlTOstr(all_user[x])
            msgs = sqlTOstr(all_msgs[x])
            try:
                the_list += f'{str(x + 1)}. <@{user}> - **{msgs} messages **\n'
            except:
                pass
        return the_list
    except:
        return None

def vcleaderboard(guildid):
    conn, c = connect(guildid)
    try:
        c.execute('SELECT userid FROM vcTime ORDER BY vc DESC')
        all_user = c.fetchall()
        c.execute('SELECT vc FROM vcTime ORDER BY vc DESC')
        all_vc = c.fetchall()

        if len(all_user) < 10:
            listrange = len(all_user)
        else:
            listrange = 10

        the_vclist = ''
        for x in range(listrange):
            user = sqlTOstr(all_user[x])
            vc = sqlTOstr(all_vc[x])
            vc = int(vc)
            vchours = 0

            while vc > 60:
                vchours += 1
                vc -= 60

            try:
                the_vclist += f'{str(x + 1)}. <@{user}> - **{vchours} hours and {vc} minutes **\n'
            except:
                pass
        return the_vclist
    except:
        return None

def tvcleaderboard(guildid):
    conn, c = connect(guildid)
    try:
        c.execute('SELECT userid FROM totalvcTime ORDER BY tvc DESC')
        all_user = c.fetchall()
        c.execute('SELECT tvc FROM totalvcTime ORDER BY tvc DESC')
        all_vc = c.fetchall()

        if len(all_user) < 10:
            listrange = len(all_user)
        else:
            listrange = 10

        the_vclist = ''
        for x in range(listrange):
            user = sqlTOstr(all_user[x])
            vc = sqlTOstr(all_vc[x])
            vc = int(vc)
            vchours = 0

            while vc > 60:
                vchours += 1
                vc -= 60

            try:
                the_vclist += f'{str(x + 1)}. <@{user}> - **{vchours} hours and {vc} minutes **\n'
            except:
                pass
        return the_vclist
    except:
        return None

def vcount(userid, guildid):
    conn, c = connect(guildid)
    try:
        c.execute("SELECT vc FROM vcTime WHERE userid = ?", (userid,))
        vcount = c.fetchone()
        c.execute("SELECT tvc from totalvcTime WHERE userid = ?", (userid,))
        tvcount = c.fetchone()

        if vcount is None:
            vcount = 0
            
        if tvcount is None:
            tvcount = 0

        uvctime = int(sqlTOstr(vcount))
        tuvctime = int(sqlTOstr(tvcount))
        userhours = 0
        tuserhours = 0

        while uvctime > 60:
            userhours += 1
            uvctime -= 60

        while tuvctime > 60:
            tuserhours += 1
            tuvctime -= 60

        return userhours, uvctime, tuserhours, tuvctime
    except:
        return None

##---------- EMBED -----------##
def successEmbed(ctx, content, title):
    embed = discord.Embed(title='', description=content, color=3211008)
    embed.set_author(name=title, icon_url=ctx.author.avatar_url)            
    return embed

def errorEmbed(ctx, content, title):
    embed = discord.Embed(title='', description=content, color=16711680)
    embed.set_author(name=title, icon_url=ctx.author.avatar_url)            
    return embed

def systemEmbed(content):
    embed = discord.Embed(title='', description=content, color=3037421)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    return embed

def messageEmbed(ctx, userid, messages, tmessages):
    embed = discord.Embed(title='', description=f"**Weekly:** \n**{messages}** messages \n\n**Total:** \n**{tmessages}** messages", color=9498256)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s # of messages""", icon_url=member.avatar_url)      
    return embed

def vcEmbed(ctx, userid, hours, minutes, thours, tminutes):
    embed = discord.Embed(title='', description=f"**Weekly:** \n**{hours}** hours and **{minutes}** minutes \n\n**Total:** \n**{thours}** hours and **{tminutes}** minutes", color=9498256)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s vc time""", icon_url=member.avatar_url)      
    return embed

def lbEmbed(ctx, title, lb):
    embed = discord.Embed(title='', description=lb, color=9498256)
    embed.set_author(name=f"""{ctx.guild.name}'s {title} Leaderboard""", icon_url=ctx.guild.icon_url)      
    return embed

##---------- CHECK -----------##
def validColor(hexid):
    try:
        color = int(hexid.replace("#", ""), base=16)
        return True, color
    except:
        return False, None

##-------------------------------------------------- COMMANDS ---------------------------------------------------##

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to discord')
    await updatestatus()

##---------- HELP ----------##
@bot.command(aliases=['h'])
async def help(ctx):
    helpe = discord.Embed(title='', description="prefix: eb ___", color=3037421)
    helpe.set_author(name="Ebyk Bot Help Page", icon_url=bot.user.avatar_url)
    helpe.set_footer(text="Programmed by ebyk#0007, dm for questions.")
    helpe.add_field(name='eb help (eb h)', value='open help menu', inline=False)
    helpe.add_field(name='eb test', value='test if the bot is online', inline=False)
    helpe.add_field(name='eb avatar (eb av)', value='check your pfp', inline=False)
    helpe.add_field(name='eb userinfo (eb whois)', value='get information about a user', inline=False)
    helpe.add_field(name='eb boosts', value='get server boost information', inline=False)
    helpe.add_field(name='eb messages (eb m, eb msg)', value='check how many messages you sent', inline=False)
    helpe.add_field(name='eb mleaderboard (eb mlb)', value='check the weekly message leaderboard', inline=False)
    helpe.add_field(name='eb tmleaderboard (eb tmlb)', value='check the total message leaderboard', inline=False)
    helpe.add_field(name='eb vc', value='check how much time you spent in vc', inline=False)
    helpe.add_field(name='eb vcleaderboard (eb vclb)', value='check the weekly vc leaderboard', inline=False)
    helpe.add_field(name='eb tvcleaderboard (eb tvclb)', value='check the total vc leaderboard', inline=False)
    helpe.set_footer(text="Join Support Server: https://discord.gg/prcN3AtNcZ")
    await ctx.channel.send(content=None, embed=helpe)

##---------- TEST -----------##
@commands.guild_only()
@bot.command()
async def test(ctx):
    embed = systemEmbed(f"""responding!""")
    await ctx.send(content=None, embed=embed)

##---------- GUILDS -----------##
@commands.guild_only()
@bot.command()
async def guilds(ctx):
    guilds = len(bot.guilds)
    embed = systemEmbed(f"""Currently in **{guilds}** servers.""")
    await ctx.send(content=None, embed=embed)

##---------- GUILDS INFO -----------##
@commands.guild_only()
@commands.is_owner()
@bot.command()
async def guildinfo(ctx):
    guilds = len(bot.guilds)
    embed = systemEmbed(f"""Currently in **{guilds}** servers.""")
    for server in bot.guilds:
        embed.add_field(name=server.name, value=f'**Owner:** {server.owner} **Members:** {server.member_count} **id:** {server.id}', inline=False)
    await ctx.send(content=None, embed=embed)

##---------- INVITE -----------##
@commands.guild_only()
@bot.command()
async def invite(ctx):
    embed = systemEmbed('**Invite:** https://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=650304&scope=bot\nadd + dm **ebyk#0007** for questions or suggestions')
    await ctx.send(content=None, embed=embed)

##---------- AVATAR -----------##
@commands.guild_only()
@bot.command(aliases=['av'])
async def avatar(ctx, member : discord.Member=None):
    try:
        userave = discord.Embed(title='', description=f"""<@{member.id}>'s pfp""", color=16580705)
        userave.set_image(url=member.avatar_url)
    except:
        userave = discord.Embed(title='', description=f"""<@{ctx.author.id}>'s pfp""", color=16580705)
        userave.set_image(url=ctx.author.avatar_url)
    userave.set_footer(text=f"""requested by {ctx.author}""")
    await ctx.send(content=None, embed=userave)


##---------- Message Count ----------##
@commands.guild_only()
@bot.command(aliases=['msg', 'messages'])
async def m(ctx, member : discord.Member=None):
    if member == None:
        userid = ctx.author.id
    else:
        userid = member.id
    umsgcount, tmsgcount = messagecount(userid, ctx.guild.id)

    embed = messageEmbed(ctx, userid, umsgcount, tmsgcount)
    await ctx.send(content=None, embed=embed)

##---------- Message Leaderboard ----------##
@commands.guild_only()
@bot.command(aliases=['mleaderboard'])
async def mlb(ctx):
    lb = messageleaderboard(ctx.guild.id)
    embed = lbEmbed(ctx, "Weekly", lb)
    await ctx.send(content=None, embed=embed)

##---------- Total Message Leaderboard ----------##
@commands.guild_only()
@bot.command(aliases=['totalmleaderboard'])
async def tmlb(ctx):
    lb = tmessageleaderboard(ctx.guild.id)
    embed = lbEmbed(ctx, "Total", lb)
    await ctx.send(content=None, embed=embed)

##---------- Vc Time ----------##
@commands.guild_only()
@bot.command()
async def vc(ctx, member : discord.Member=None, not_required=None):
    if member == None:
        userid = ctx.author.id
    else:
        userid = member.id
    hours, minutes, thours, tminutes = vcount(userid, ctx.guild.id)
    embed = vcEmbed(ctx, userid, hours, minutes, thours, tminutes)
    await ctx.send(content=None, embed=embed)

##---------- Vc Time Leaderboard ----------##
@commands.guild_only()
@bot.command()
async def vclb(ctx):
    lb = vcleaderboard(ctx.guild.id)
    embed = lbEmbed(ctx, "Weekly", lb)
    await ctx.send(content=None, embed=embed)

##---------- Total Vc Time Leaderboard ----------##
@commands.guild_only()
@bot.command()
async def tvclb(ctx):
    lb = tvcleaderboard(ctx.guild.id)
    embed = lbEmbed(ctx, "Total", lb)
    await ctx.send(content=None, embed=embed)

##---------- LEADERBOARD RESET -----------##
@commands.guild_only()
@commands.is_owner()
@bot.command()
async def lbreset(ctx):
    for filename in os.listdir('/home/ebyk/ebykdb'):
        conn = sqlite3.connect(f"/home/ebyk/ebykdb/{filename}")
        c = conn.cursor()
        try:
            c.execute('UPDATE msgCount SET msgs = 0 WHERE msgs < 999999')
            c.execute('UPDATE vcTime SET vc = 0 WHERE vc < 999999')
            conn.commit()
            print(f"Leaderboard Reset Succeeded for {filename}")
        except:
            print(f"Leaderboard Reset Failed for {filename}")

##---------- Userinfo -----------##
@commands.guild_only()
@bot.command(aliases=['whois'])
async def userinfo(ctx, member : discord.Member=None):    
    if member is None:
        member = ctx.author
    conn, c = connect(ctx.guild.id)
    pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
    posreal = pos + 1
           
    msgcount, tmsgcount = messagecount(member.id, ctx.guild.id)
    userhours, usermins, tuserhours, tusermins = vcount(member.id, ctx.guild.id)
    
    whois = discord.Embed(title='', description=f"""<@{member.id}>""", color=10181046)
    whois.set_author(name=member, icon_url=member.avatar_url)
    whois.set_thumbnail(url=member.avatar_url)
    whois.add_field(name='User ID', value=member.id, inline=False)
    whois.add_field(name='Joined Server', value=member.joined_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)
    whois.add_field(name='Created Account', value=member.created_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)

    if not member.bot:
        whois.add_field(name='Total Messages', value=f"""**{tmsgcount}** messages""", inline=False)
        whois.add_field(name='Total VC Time', value=f"""**{tuserhours}** hours and **{tusermins}** minutes""", inline=False)
        whois.add_field(name='Account Type', value=f"""user""", inline=False)
        whois.add_field(name='Highest Role', value=f"""{member.top_role.mention}""", inline=False)
    else:
        whois.add_field(name='Account Type', value=f"""bot""", inline=False)

    whois.add_field(name='Join Position', value=posreal)
    await ctx.send(content=None, embed=whois)

##---------- NITROBOOST -----------##
@commands.guild_only()
@bot.command()
async def boosts(ctx):
    members = []
    for member in ctx.author.guild.premium_subscribers:
        members.append(f'<@{member.id}>')
        members = [str(members).replace('[','').replace(']','').replace("'",'').replace("'",'')]
    members = str(members).replace('[','').replace(']','').replace("'",'').replace("'",'')
    nitro = discord.Embed(title='', description=f"""**Tier:** level {ctx.author.guild.premium_tier} \n**Boosts:** {ctx.author.guild.premium_subscription_count} \n**Boosters:** {members}""", color=16580705)

    nitro.set_author(name=f"{ctx.guild.name}'s Nitro Boost Status", icon_url=ctx.guild.icon_url)
    nitro.set_thumbnail(url='https://cdn.discordapp.com/emojis/689542582987915438.gif?v=1')
    await ctx.send(content=None, embed=nitro)

##---------- Bot Events ----------##
@bot.event
async def on_guild_join(guild):
    try:
        filename = f"/home/ebyk/ebykdb/({guild.id}) sql.db"
        conn = sqlite3.connect(filename)
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS msgCount(userid VARCHAR(255), msgs INT)')
        c.execute('CREATE TABLE IF NOT EXISTS totalmsgCount(userid VARCHAR(255), tmsgs INT)')
        c.execute('CREATE TABLE IF NOT EXISTS vcTime(userid VARCHAR(255), vc INT)')
        c.execute('CREATE TABLE IF NOT EXISTS "totalvcTime"("userid" VARCHAR(255), "tvc" INT)')
        c.execute('CREATE TABLE IF NOT EXISTS timeLog(userid VARCHAR(255), jTime DATETIME)')
        c.execute('CREATE TABLE IF NOT EXISTS partnerCount(userid VARCHAR(255), partners INT)')
        conn.commit()
    except:
        filename = f"/home/ebyk/ebykdb/({guild.id}) sql.db"
        open(filename)
    await updatestatus()

@bot.event
async def on_guild_remove(guild):
    await updatestatus()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot:
        return

    if bot.user.mentioned_in(message) and not message.mention_everyone:
        embed = systemEmbed("**prefix:** eb ___\nSend `eb help` for my help menu!")
        await message.channel.send(content=None, embed=embed)

    if message.guild is None and message.author is not bot.user and not 'eb help' in message.content.lower():
        await message.author.send("Hey I'm Ebyk Bot, run the command **eb help** to check out what I offer!")
        return

    conn, c = connect(message.guild.id)

    c.execute("SELECT msgs FROM msgCount WHERE userid = ?", (message.author.id,))
    count = c.fetchone()
    c.execute("SELECT tmsgs FROM totalmsgCount WHERE userid = ?", (message.author.id,))
    tcount = c.fetchone()

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

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    conn, c = connect(member.guild.id)
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

@tasks.loop(hours=12.0)
async def checkday():
    await bot.wait_until_ready()
    day = datetime.datetime.today().strftime('%A')
    if day == "Sunday":
        resetlb()


checkday.start()

token = read_token()
bot.run(token)