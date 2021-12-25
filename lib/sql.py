import os
import sqlite3

dbdir = "/home/ebyk/EbykBot/ebykdb/"
#dbdir = "/Users/personal/Documents/GitHub/EbykBot/ebykdb/"

##---------- SQL CONNECT -----------##
def connect(guildid):
    filename = f"{dbdir}({guildid}) sql.db"
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

def resetlb():
    for filename in os.listdir(dbdir):
        conn = sqlite3.connect(f"{dbdir}{filename}")
        c = conn.cursor()
        try:
            c.execute('UPDATE msgCount SET msgs = 0 WHERE msgs < 999999')
            c.execute('UPDATE vcTime SET vc = 0 WHERE vc < 999999')
            conn.commit()
            print(f"Leaderboard Reset Succeeded for {filename}")
        except:
            print(f"Leaderboard Reset Failed for {filename}")

def resetdlb():
    for filename in os.listdir(dbdir):
        conn = sqlite3.connect(f"{dbdir}{filename}")
        c = conn.cursor()
        try:
            c.execute('UPDATE dmsgCount SET dmsgs = 0 WHERE dmsgs < 999999')
            conn.commit()
            print(f"Leaderboard Reset Succeeded for {filename}")
        except:
            print(f"Leaderboard Reset Failed for {filename}")
            
def resettmlb(guildid):
    filename = f"{dbdir}({guildid}) sql.db"
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    try:
        c.execute('UPDATE totalmsgCount SET tmsgs = 0 WHERE tmsgs < 999999')
        conn.commit()
        print(f"Total Message Leaderboard Reset Succeeded for {filename}")
    except:
        print(f"Total Message Leaderboard Reset Failed for {filename}")

def resettvclb(guildid):
    filename = f"{dbdir}({guildid}) sql.db"
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    try:
        c.execute('UPDATE totalvcTime SET tvc = 0 WHERE tvc < 999999')
        conn.commit()
        print(f"Total Voice Leaderboard Reset Succeeded for {filename}")
    except:
        print(f"Total Voice Leaderboard Reset Failed for {filename}")

def newdbfile(guildid):
    filename = f"{dbdir}({guildid}) sql.db"
    open(filename)