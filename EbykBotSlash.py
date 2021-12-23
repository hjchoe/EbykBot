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
from threading import Thread
from multiprocessing import Process
intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='.', case_insensitive=True, owner_id=329326685185114115, help_command=None, intents=intents)

##-------------------------------------------------- DEFINITIONS ---------------------------------------------------##

def read_token():
    with open("testtoken.txt", "r") as f:
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

def resetdlb():
    for filename in os.listdir('/home/ebyk/ebykdb'):
        conn = sqlite3.connect(f"/home/ebyk/ebykdb/{filename}")
        c = conn.cursor()
        try:
            c.execute('UPDATE dmsgCount SET dmsgs = 0 WHERE dmsgs < 999999')
            conn.commit()
            print(f"Leaderboard Reset Succeeded for {filename}")
        except:
            print(f"Leaderboard Reset Failed for {filename}")
            
def resettmlb(guildid):
    filename = f"/home/ebyk/ebykdb/({guildid}) sql.db"
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    try:
        c.execute('UPDATE totalmsgCount SET tmsgs = 0 WHERE tmsgs < 999999')
        conn.commit()
        print(f"Total Message Leaderboard Reset Succeeded for {filename}")
    except:
        print(f"Total Message Leaderboard Reset Failed for {filename}")

def resettvclb(guildid):
    filename = f"/home/ebyk/ebykdb/({guildid}) sql.db"
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    try:
        c.execute('UPDATE totalvcTime SET tvc = 0 WHERE tvc < 999999')
        conn.commit()
        print(f"Total Voice Leaderboard Reset Succeeded for {filename}")
    except:
        print(f"Total Voice Leaderboard Reset Failed for {filename}")

async def updatestatus():
    totalusers = 0
    for server in bot.guilds:
        totalusers += len(server.members)
    activity = discord.Game(name=f"{totalusers} users! | eb h for help")
    await bot.change_presence(status=discord.Status.online, activity=activity)

##---------- SQL CONNECT -----------##
def connect(guildid):
    filename = f"/home/ebyk/ebykdb/({guildid}) sql.db"
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS msgCount(userid VARCHAR(255), msgs INT)')
    c.execute('CREATE TABLE IF NOT EXISTS totalmsgCount(userid VARCHAR(255), tmsgs INT)')
    c.execute('CREATE TABLE IF NOT EXISTS dmsgCount(userid VARCHAR(255), dmsgs INT)')
    c.execute('CREATE TABLE IF NOT EXISTS vcTime(userid VARCHAR(255), vc INT)')
    c.execute('CREATE TABLE IF NOT EXISTS "totalvcTime"("userid" VARCHAR(255), "tvc" INT)')
    c.execute('CREATE TABLE IF NOT EXISTS timeLog(userid VARCHAR(255), jTime DATETIME)')
    c.execute('CREATE TABLE IF NOT EXISTS partnerCount(userid VARCHAR(255), partners INT)')
    c.execute('CREATE TABLE IF NOT EXISTS bank(userid VARCHAR(255), money INT)')
    c.execute('CREATE TABLE IF NOT EXISTS deletedmsg(channelid VARCHAR(255), userid VARCHAR(255), content VARCHAR(255))')
    c.execute('CREATE TABLE IF NOT EXISTS editedmsg(channelid VARCHAR(255), userid VARCHAR(255), before VARCHAR(255), after VARCHAR(255))')
    conn.commit()
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
        c.execute("SELECT dmsgs from dmsgCount WHERE userid = ?", (userid,))
        dcount = c.fetchone()

        if count is None:
            count = 0

        if tcount is None:
            tcount = 0

        if dcount is None:
            dcount = 0

        umsgcount = sqlTOstr(count)
        tmsgcount = sqlTOstr(tcount)
        dmsgcount = sqlTOstr(dcount)
        return umsgcount, tmsgcount, dmsgcount
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

def dmessageleaderboard(guildid):
    conn, c = connect(guildid)
    try:
        c.execute('SELECT userid FROM dmsgCount ORDER BY dmsgs DESC')
        all_user = c.fetchall()
        c.execute('SELECT dmsgs FROM dmsgCount ORDER BY dmsgs DESC')
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

def balancegrab(userid, guildid):
    conn, c = connect(guildid)
    try:
        c.execute("SELECT money FROM bank WHERE userid = ?", (userid,))
        count = c.fetchone()

        if count is None:
            count = 0

        money = sqlTOstr(count)
        return money
    except:
        return None

def balleaderboard(guildid):
    conn, c = connect(guildid)
    try:
        c.execute('SELECT userid FROM bank ORDER BY money DESC')
        all_user = c.fetchall()
        c.execute('SELECT money FROM bank ORDER BY money DESC')
        all_bals = c.fetchall()

        if len(all_user) < 10:
            listrange = len(all_user)
        else:
            listrange = 10
        the_list = ''
        for x in range(listrange):
            user = sqlTOstr(all_user[x])
            bals = sqlTOstr(all_bals[x])
            try:
                the_list += f'{str(x + 1)}. <@{user}> - **${bals}**\n'
            except:
                pass
        return the_list
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

def messageEmbed(ctx, userid, messages, tmessages, dmessages):
    embed = discord.Embed(title='', description=f"**Daily:** {dmessages} messages\n**Weekly:** {messages} messages\n**Total:** {tmessages} messages", color=16645526)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s # of messages""", icon_url=member.avatar_url)
    return embed

def vcEmbed(ctx, userid, hours, minutes, thours, tminutes):
    embed = discord.Embed(title='', description=f"**Weekly:** \n**{hours}** hours and **{minutes}** minutes \n\n**Total:** \n**{thours}** hours and **{tminutes}** minutes", color=16645526)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s vc time""", icon_url=member.avatar_url)
    return embed

def lbEmbed(ctx, title, lb):
    embed = discord.Embed(title='', description=lb, color=13276925)
    embed.set_author(name=f"""{ctx.guild.name}'s {title} Leaderboard""", icon_url=ctx.guild.icon_url)
    return embed

def balEmbed(ctx, userid, amt):
    embed = discord.Embed(title='', description=f"Balance: **${amt}**", color=16645526)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s Bank""", icon_url=member.avatar_url)
    return embed

def coinflipEmbed(ctx, userid, win, side, coin, betamt, amt):
    if win == True:
        color = 9498256
        win = "WON"
    else:
        color = 16619158
        win = "LOST"
    embed = discord.Embed(title='', description=f"**Guess:** {side}\n**Coin:** {coin}\n**Result:** {win}\n**Amount Bet:** ${betamt}\n**New Balance:** ${amt}", color=color)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s Result""", icon_url=member.avatar_url)
    return embed

def giveEmbed(ctx, userid, memberid, amt):
    receiver = discord.utils.get(ctx.author.guild.members, id=memberid)
    embed = discord.Embed(title='', description=f"{ctx.author.mention} gave {receiver.mention} **${amt}**", color=16645526)
    giver = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""Money Transfer""", icon_url=giver.avatar_url)
    return embed

def snipeEmbed(ctx, userid, content):
    embed = discord.Embed(title='', description=content, color=16760576)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name} [{member.id}]""", icon_url=member.avatar_url)
    embed.set_footer(text=f"sniped by: {ctx.author.name} [{ctx.author.id}]")
    return embed

def esnipeEmbed(ctx, userid, beforecontent, aftercontent):
    embed = discord.Embed(title='', description=f"**Before:** {beforecontent}\n**After:** {aftercontent}", color=16760576)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name} [{member.id}]""", icon_url=member.avatar_url)
    embed.set_footer(text=f"sniped by: {ctx.author.name} [{ctx.author.id}]")
    return embed

##---------- CHECK -----------##
def validColor(hexid):
    try:
        color = int(hexid.replace("#", ""), base=16)
        return True, color
    except:
        return False, None

# betting #

def flipcoin():
    choices = ["heads", "tails"]
    result = choices[random.randint(0, 1)]
    return result

def checkbal(bank):
    bank = int(bank)
    if bank <= 0.0:
        playstatus = False
    else:
        playstatus = True
    return playstatus, bank

def checkwager(wager, bank):
    bank = int(bank)
    try:
        wager = int(wager)
        if wager > bank:
            wagerstatus = False
        else:
            wagerstatus = True
        return wagerstatus, wager
    except:
        return None, wager

def checkgiveamt(amt, bank):
    bank = int(bank)
    try:
        amt = int(amt)
        if amt > bank:
            amtstatus = False
        else:
            amtstatus = True
        return amtstatus, amt
    except:
        return None, amt

def checkwin(choice, result):
    if choice == result:
        win = True
    else:
        win = False
    return win

def checkside(side):
    possible = ["heads", "tails", "h", "t"]
    if side.lower() in possible:
        return True
    else:
        return False

def transaction(userid, guildid, win, betamt, bank):
    bank = int(bank)
    betamt = int(betamt)
    if win == True:
        bank += betamt
    else:
        bank -= betamt
    conn, c = connect(guildid)
    try:
        c.execute('UPDATE bank SET money = ? WHERE userid = ?', (bank, userid))
        conn.commit()
    except:
        pass
    return bank

def givetransaction(userid, memberid, guildid, amount):
    ubank = balancegrab(userid, guildid)
    rbank = balancegrab(memberid, guildid)
    ubank = int(ubank)
    rbank = int(rbank)
    amount = int(amount)
    ubank -= amount
    rbank += amount
    conn, c = connect(guildid)
    try:
        c.execute('UPDATE bank SET money = ? WHERE userid = ?', (ubank, userid))
        c.execute('UPDATE bank SET money = ? WHERE userid = ?', (rbank, memberid))
        conn.commit()
    except:
        pass

def snipecountdown(message):
    time.sleep(10)
    channelid = message.channel.id
    conn, c = connect(message.guild.id)
    try:
        c.execute('DELETE FROM deletedmsg WHERE channelid = ?', (channelid,))
        conn.commit()
    except:
        pass

def esnipecountdown(message):
    time.sleep(10)
    channelid = message.channel.id
    conn, c = connect(message.guild.id)
    try:
        c.execute('DELETE FROM editedmsg WHERE channelid = ?', (channelid,))
        conn.commit()
    except:
        pass

##-------------------------------------------------- COMMANDS ---------------------------------------------------##

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to discord')
    await updatestatus()

##---------- HELP ----------##
@bot.command(aliases=['h'])
async def help(ctx, htype=None):
    helpe = discord.Embed(title='', description="prefix: eb ___", color=3037421)
    helpe.set_author(name="Ebyk Bot Help Page", icon_url=bot.user.avatar_url)
    helpe.set_footer(text="Programmed by ebyk#7894, dm for questions.")
    if htype == None:
        helpe.add_field(name='eb h general', value='open general commands help menu', inline=False)
        helpe.add_field(name='eb h leaderboards', value='open message/vc leaderboards help menu', inline=False)
        helpe.add_field(name='eb h gambling', value='open gambling help menu', inline=False)
    elif htype == "general":
        helpe.add_field(name='eb help (eb h)', value='open help menu', inline=False)
        helpe.add_field(name='eb test', value='test if the bot is online', inline=False)
        helpe.add_field(name='eb avatar (eb av)', value='check your pfp', inline=False)
        helpe.add_field(name='eb userinfo (eb whois)', value='get information about a user', inline=False)
        helpe.add_field(name='eb serverinfo (eb sf)', value='get information about a server', inline=False)
        helpe.add_field(name='eb boosts', value='get server boost information', inline=False)
        helpe.add_field(name='eb snipe', value='sends last message that was deleted in the channel (within 10 seconds)', inline=False)
    elif htype == "leaderboards":
        helpe.add_field(name='eb messages (eb m, eb msg)', value='check how many messages you sent', inline=False)
        helpe.add_field(name='eb mleaderboard (eb mlb)', value='check the weekly message leaderboard', inline=False)
        helpe.add_field(name='eb tmleaderboard (eb tmlb)', value='check the total message leaderboard', inline=False)
        helpe.add_field(name='eb dmleaderboard (eb dmlb)', value='check the daily message leaderboard', inline=False)
        helpe.add_field(name='eb vc', value='check how much time you spent in vc', inline=False)
        helpe.add_field(name='eb vcleaderboard (eb vclb)', value='check the weekly vc leaderboard', inline=False)
        helpe.add_field(name='eb tvcleaderboard (eb tvclb)', value='check the total vc leaderboard', inline=False)
        helpe.add_field(name='eb reset_total_mlb (eb rtmlb)', value='reset the total leaderboard for messages, requires Admin Permission', inline=False)
        helpe.add_field(name='eb reset_total_vclb (eb rtvclb)', value='reset the total leaderboard for voice, requires Admin Permission', inline=False)        
        helpe.add_field(name='eb removemessages (eb rm)', value='remove total messages from a member, requires Admin Permission', inline=False)        
    elif htype == "gambling":
        helpe.add_field(name='eb balance (eb bal)', value='check your balance', inline=False)
        helpe.add_field(name='eb bleaderboard (eb blb)', value='check the server balance leaderboard', inline=False)
        helpe.add_field(name='eb coinflip (eb cf)', value='bet and gamble your money on a coin flip', inline=False)
        helpe.add_field(name='eb give (eb g)', value='give somebody a certain amount from your bank', inline=False)

    helpe.set_footer(text="Join Support Server: https://discord.gg/prcN3AtNcZ")
    await ctx.channel.send(content=None, embed=helpe)

##---------- TEST -----------##
@commands.guild_only()
@bot.command()
async def test(ctx):
    latency = round(bot.latency * 1000)
    embed = systemEmbed(f"""responding!\n\n**Ping: **{latency}ms""")
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

##---------- Manual Daily LB Reset -----------##
@commands.guild_only()
@commands.is_owner()
@bot.command()
async def manu_dlb_reset(ctx):
    resetdlb()
    embed = systemEmbed("Attempted manual reset of daily leaderboard")
    await ctx.send(content=None, embed=embed)
    
##---------- Admin Total Message LB Reset -----------##
@commands.guild_only()
@commands.has_permissions(administrator=True)
@bot.command(aliases=['rtmlb'])
async def reset_total_mlb(ctx):
    resettmlb(ctx.guild.id)
    embed = systemEmbed("Finished manual reset of total message leaderboard")
    await ctx.send(content=None, embed=embed)
    
@reset_total_mlb.error
async def reset_total_mlb_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = errorEmbed(ctx, "Failed to reset total message leaderboard", "Missing Admin Permissions")
        await ctx.send(content=None, embed=embed)

##---------- Admin Total Voice LB Reset -----------##
@commands.guild_only()
@commands.has_permissions(administrator=True)
@bot.command(aliases=['rtvclb'])
async def reset_total_vclb(ctx):
    resettvclb(ctx.guild.id)
    embed = systemEmbed("Finished manual reset of total voice leaderboard")
    await ctx.send(content=None, embed=embed)
    
@reset_total_vclb.error
async def reset_total_vclb_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = errorEmbed(ctx, "Failed to reset total voice leaderboard", "Missing Admin Permissions")
        await ctx.send(content=None, embed=embed)
        
##---------- Admin Message Remove -----------##
@commands.guild_only()
@commands.has_permissions(administrator=True)
@bot.command(aliases=['rm'])
async def removemessages(ctx, member : discord.Member, messages):
    conn, c = connect(ctx.guild.id)
    c.execute("SELECT tmsgs from totalmsgCount WHERE userid = ?", (member.id,))
    tcount = c.fetchone()
    if int(messages) > int(tcount[0]):
        newtcount = 0;
        c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (newtcount, member.id))
        conn.commit()
    else:
        newtcount = int(tcount[0])-int(messages)
        c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (newtcount, member.id))
        conn.commit()

    embed = systemEmbed(f"Removed {messages} messages from {member.mention}. They are now at {newtcount} messages.")
    await ctx.send(content=None, embed=embed)

@removemessages.error
async def removemessages_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = errorEmbed(ctx, "Failed to remove messages.", "Missing Admin Permissions")
        await ctx.send(content=None, embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = errorEmbed(ctx, "Proper usage is: eb removemessages @user numberofmessages", "Incorrect Syntax")
        await ctx.send(content=None, embed=embed)

##---------- INVITE -----------##
@commands.guild_only()
@bot.command()
async def invite(ctx):
    embed = systemEmbed('**Invite:** https://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=650304&scope=bot\nadd + dm **ebyk#1660** for questions or suggestions')
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
    umsgcount, tmsgcount, dmsgcount = messagecount(userid, ctx.guild.id)

    embed = messageEmbed(ctx, userid, umsgcount, tmsgcount, dmsgcount)
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
@bot.command(aliases=['tmleaderboard'])
async def tmlb(ctx):
    lb = tmessageleaderboard(ctx.guild.id)
    embed = lbEmbed(ctx, "Total", lb)
    await ctx.send(content=None, embed=embed)

##---------- Daily Message Leaderboard ----------##
@commands.guild_only()
@bot.command(aliases=['dmleaderboard'])
async def dmlb(ctx):
    lb = dmessageleaderboard(ctx.guild.id)
    embed = lbEmbed(ctx, "Daily", lb)
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

    msgcount, tmsgcount, dmsgcount = messagecount(member.id, ctx.guild.id)
    userhours, usermins, tuserhours, tusermins = vcount(member.id, ctx.guild.id)
    bal = balancegrab(member.id, ctx.guild.id)

    whois = discord.Embed(title='', description=f"""<@{member.id}>""", color=10181046)
    whois.set_author(name=member, icon_url=member.avatar_url)
    whois.set_thumbnail(url=member.avatar_url)
    whois.add_field(name='User ID', value=member.id, inline=False)
    whois.add_field(name='Joined Server', value=member.joined_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)
    whois.add_field(name='Created Account', value=member.created_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)

    if not member.bot:
        whois.add_field(name='Total Messages', value=f"""**{tmsgcount}** messages""", inline=False)
        whois.add_field(name='Total VC Time', value=f"""**{tuserhours}** hours and **{tusermins}** minutes""", inline=False)
        whois.add_field(name='Total Balance', value=f"""**${bal}**""", inline=False)
        whois.add_field(name='Account Type', value=f"""user""", inline=False)
        whois.add_field(name='Highest Role', value=f"""{member.top_role.mention}""", inline=False)
    else:
        whois.add_field(name='Account Type', value=f"""bot""", inline=False)

    whois.add_field(name='Join Position', value=posreal)
    await ctx.send(content=None, embed=whois)

##---------- serverinfo -----------##
@commands.guild_only()
@bot.command(aliases=['sf'])
async def serverinfo(ctx):
    guild = ctx.guild

    whois = discord.Embed(title='', description=guild.description, color=16632470)
    whois.set_author(name=guild.name, icon_url=guild.icon_url)
    whois.set_thumbnail(url=guild.icon_url)
    try:
        whois.set_image(url=guild.banner_url)
    except:
        pass

    whois.add_field(name='Owner', value=f"{guild.owner.mention} [{guild.owner_id}]", inline=False)
    whois.add_field(name='Id', value=guild.id, inline=False)
    whois.add_field(name='Created On', value=guild.created_at.strftime("%b %d %Y [*%H:%M:%S*]"), inline=False)
    whois.add_field(name='Region', value=guild.region, inline=False)

    whois.add_field(name='Stats', value=f"**Members:** {guild.member_count}\n**Categories:** {len(guild.categories)}\n**Text Channels:** {len(guild.text_channels)}\n**Voice Channels:** {len(guild.voice_channels)}\n**Roles:** {len(guild.roles)}\n**Emojis:** {len(guild.emojis)}", inline=False)

    whois.add_field(name='Nitro Server Boosts', value=f"**Tier:** {guild.premium_tier}\n**Boosters:** {guild.premium_subscription_count}", inline=False)

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

##---------- coinflip ----------##
@commands.guild_only()
@bot.command(aliases=['cf'])
async def coinflip(ctx, side, betamount):
    bank = balancegrab(ctx.author.id, ctx.guild.id)
    wagerstatus, betamount = checkwager(betamount, bank)
    if wagerstatus == True:
        playstatus, bank = checkbal(bank)
        if playstatus == True:
            sidestatus = checkside(side)
            if sidestatus == True:
                coin = flipcoin()
                win = checkwin(side, coin)
                bank = transaction(ctx.author.id, ctx.guild.id, win, betamount, bank)
                embed = coinflipEmbed(ctx, ctx.author.id, win, side, coin, betamount, bank)
            elif sidestatus == False:
                embed = errorEmbed(ctx, f"You have entered an invalid side of the coin. Choose heads or tails.", "Invalid Input Error")
        elif playstatus == False:
            embed = errorEmbed(ctx, f"You do not have enough funds to play. Balance: **${bank}**", "Balance Error")
    elif wagerstatus == False:
        embed = errorEmbed(ctx, f"You can't bet more than you have. Balance: **${bank}**", "Wager Error")
    else:
        embed = errorEmbed(ctx, "Enter a proper integer to bet.", "Invalid Betting Amount Error")
    await ctx.send(content=None, embed=embed)

@coinflip.error
async def coinflip_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = errorEmbed(ctx, "Please use the command properly: `.cf coinside betamount`", "Invalid Command Error")
        await ctx.send(content=None, embed=embed)

##---------- Balance Check ----------##
@commands.guild_only()
@bot.command(aliases=['bal', 'b'])
async def balance(ctx, member : discord.Member=None):
    if member == None:
        userid = ctx.author.id
    else:
        userid = member.id
    moneyamt = balancegrab(userid, ctx.guild.id)

    embed = balEmbed(ctx, userid, moneyamt)
    await ctx.send(content=None, embed=embed)

##---------- Balance Leaderboard ----------##
@commands.guild_only()
@bot.command(aliases=['bleaderboard'])
async def blb(ctx):
    lb = balleaderboard(ctx.guild.id)
    embed = lbEmbed(ctx, "Bank", lb)
    await ctx.send(content=None, embed=embed)

##---------- give ----------##
@commands.guild_only()
@bot.command(aliases=['g'])
async def give(ctx, member : discord.Member, amount):
    bank = balancegrab(ctx.author.id, ctx.guild.id)
    amountstatus, amount = checkgiveamt(amount, bank)
    if member:
        if amountstatus == True:
            givetransaction(ctx.author.id, member.id, ctx.guild.id, amount)
            embed = giveEmbed(ctx, ctx.author.id, member.id, amount)
        elif amountstatus == False:
            embed = errorEmbed(ctx, f"You can't give more than you have. Balance: **${bank}**", "Balance Error")
        else:
            embed = errorEmbed(ctx, f"Provide a proper integer amount to give somebody", "Invalid Input Error")
    else:
        embed = errorEmbed(ctx, f"Provide a proper user to give money to", "Invalid Input Error")
    await ctx.send(content=None, embed=embed)

@give.error
async def give_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = errorEmbed(ctx, "Please use the command properly: `.give @user amount`", "Invalid Command Error")
        await ctx.send(content=None, embed=embed)
    if isinstance(error, discord.ext.commands.BadArgument):
        embed = errorEmbed(ctx, "Provide a proper user to give money to", "Invalid Input Error")
        await ctx.send(content=None, embed=embed)

##---------- Snipe -----------##
@commands.guild_only()
@bot.command()
async def snipe(ctx):
    channelid = ctx.channel.id
    conn, c = connect(ctx.guild.id)
    try:
        c.execute('SELECT content FROM deletedmsg WHERE channelid = ?', (channelid,))
        content = c.fetchone()
        c.execute('SELECT userid FROM deletedmsg WHERE channelid = ?', (channelid,))
        authorid = c.fetchone()
        content = sqlTOstr(content)
        authorid = sqlTOstr(authorid)
        authorid = int(authorid)
        embed = snipeEmbed(ctx, authorid, content)
    except:
        embed = errorEmbed(ctx, "There are no messages to snipe in this channel.", "Snipe Error")
    await ctx.send(content=None, embed=embed)

##---------- edit Snipe -----------##
@commands.guild_only()
@bot.command()
async def esnipe(ctx):
    channelid = ctx.channel.id
    conn, c = connect(ctx.guild.id)
    try:
        c.execute('SELECT before FROM editedmsg WHERE channelid = ?', (channelid,))
        beforecontent = c.fetchone()
        c.execute('SELECT after FROM editedmsg WHERE channelid = ?', (channelid,))
        aftercontent = c.fetchone()
        c.execute('SELECT userid FROM editedmsg WHERE channelid = ?', (channelid,))
        authorid = c.fetchone()
        aftercontent = sqlTOstr(aftercontent)
        beforecontent = sqlTOstr(beforecontent)
        authorid = sqlTOstr(authorid)
        authorid = int(authorid)
        embed = esnipeEmbed(ctx, authorid, beforecontent, aftercontent)
    except:
        embed = errorEmbed(ctx, "There are no messages to edit snipe in this channel.", "eSnipe Error")
    await ctx.send(content=None, embed=embed)

##---------- Update Message -----------##
@commands.is_owner()
@bot.command()
async def updatemsg(ctx):
    guilds = len(bot.guilds)
    embed = systemEmbed(f"""~ **UPDATE ANNOUNCEMENT** ~\n\nThank you for using Ebyk Bot!\nThe bot was down due to host server problems, but it has been fixed!\n""")
    embed.add_field(name="Change Log", value=f"""\n- easier to navigate help menu (run eb help to check it out)\n- simple economy and gambling\n- daily leaderboards\n\n*Join the support server at: https://discord.gg/prcN3AtNcZ*""", inline=False)
    for server in bot.guilds:
        try:
            member = discord.utils.get(server.members, id=server.owner_id)
            await member.send(content=None, embed=embed)
            print(f"message sent [{server.name}]")
            time.sleep(1)
        except:
            print(f"message FAILED [{server.name}]")
            pass
    print("done")

##---------- Update Test -----------##
@commands.is_owner()
@bot.command()
async def updatemsgtest(ctx):
    guilds = len(bot.guilds)
    embed = systemEmbed(f"""~ **UPDATE ANNOUNCEMENT** ~\n\nThank you for using Ebyk Bot!\nThe bot was down due to host server problems, but it has been fixed!\n""")
    embed.add_field(name="Change Log", value=f"""\n- easier to navigate help menu (run eb help to check it out)\n- simple economy and gambling\n- daily leaderboards\n\n*Join the support server at: https://discord.gg/prcN3AtNcZ*""", inline=False)
    await ctx.send(content=None, embed=embed)

##---------- Update Message -----------##
@commands.is_owner()
@bot.command()
async def temp(ctx):
    guilds = len(bot.guilds)
    for server in bot.guilds:
        try:
            member = discord.utils.get(server.members, id=server.owner_id)
            conn, c = connect(server.id)
            c.execute('DROP TABLE editedmsg')
            print(f"deleted in [{server.name}]")
            time.sleep(1)
        except:
            print(f"delete FAILED [{server.name}]")
            pass
    print("done")

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
        c.execute('CREATE TABLE IF NOT EXISTS bank(userid VARCHAR(255), money INT)')
        c.execute('CREATE TABLE IF NOT EXISTS deletedmsg(channelid VARCHAR(255), userid VARCHAR(255), content VARCHAR(255))')
        c.execute('CREATE TABLE IF NOT EXISTS editedmsg(channelid VARCHAR(255), userid VARCHAR(255), before VARCHAR(255), after VARCHAR(255))')
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
    ctx = await bot.get_context(message)
    if ctx.valid:
        pass
    else:
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

@bot.event
async def on_message_delete(message):
    channelid = message.channel.id
    conn, c = connect(message.guild.id)
    try:
        c.execute('SELECT content FROM deletedmsg WHERE channelid = ?', (channelid,))
        content = c.fetchone()
    except:
        pass
    if message.content == None:
        pass
    else:
        c.execute('DELETE FROM deletedmsg WHERE channelid = ?', (channelid,))
        conn.commit()
        c.execute('INSERT INTO deletedmsg (channelid, userid, content) VALUES (?,?,?)', (channelid, message.author.id, message.content))
        conn.commit()
        p = Process(target=snipecountdown, args=(message,))
        p.start()

@bot.event
async def on_message_edit(before, after):
    channelid = before.channel.id
    conn, c = connect(before.guild.id)
    try:
        c.execute('SELECT content FROM editedmsg WHERE channelid = ?', (channelid,))
        content = c.fetchone()
    except:
        pass
    if before.content == after.content:
        pass
    else:
        c.execute('DELETE FROM editedmsg WHERE channelid = ?', (channelid,))
        conn.commit()
        c.execute('INSERT INTO editedmsg (channelid, userid, before, after) VALUES (?,?,?,?)', (channelid, before.author.id, before.content, after.content))
        conn.commit()
        p = Process(target=esnipecountdown, args=(before,))
        p.start()

@tasks.loop(hours=12.0)
async def checkday():
    await bot.wait_until_ready()
    day = datetime.datetime.today().strftime('%A')
    if day == "Sunday":
        resetlb()

@tasks.loop(hours=24.0)
async def resetdailylb():
    await bot.wait_until_ready()
    resetdlb()

checkday.start()
resetdailylb.start()

token = read_token()
bot.run(token)
