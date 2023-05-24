import os
import sqlite3

#dbdir = "/home/ebyk/EbykBot/ebykdb/"
#dbdir = "/home/ebyk/EbykBot/ebykdbtest/"

#dbdir = "/Users/personal/Documents/GitHub/EbykBot/ebykdb/"
dbdir = "/Users/hjcho/Documents/GitHub/EbykBot/ebykdb"

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
    c.execute('CREATE TABLE IF NOT EXISTS dvcTime(userid VARCHAR(255), dvc INT)')
    c.execute('CREATE TABLE IF NOT EXISTS timeLog(userid VARCHAR(255), jTime DATETIME)')
    c.execute('CREATE TABLE IF NOT EXISTS bank(userid VARCHAR(255), money INT)')
    conn.commit()
    return conn, c

def glb_connect():
    filename = f"{dbdir}guildmessages.db"
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS guildmsgcount(guildid VARCHAR(255), msgs INT)')
    c.execute('CREATE TABLE IF NOT EXISTS tguildmsgcount(guildid VARCHAR(255), tmsgs INT)')
    c.execute('CREATE TABLE IF NOT EXISTS dguildmsgcount(guildid VARCHAR(255), dmsgs INT)')
    c.execute('CREATE TABLE IF NOT EXISTS guildvctime(guildid VARCHAR(255), vc INT)')
    c.execute('CREATE TABLE IF NOT EXISTS tguildvctime(guildid VARCHAR(255), tvc INT)')
    c.execute('CREATE TABLE IF NOT EXISTS dguildvctime(guildid VARCHAR(255), tvc INT)')
    c.execute('CREATE TABLE IF NOT EXISTS invitecode(guildid VARCHAR(255), code VARCHAR(255))')
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

async def messageleaderboard(bot, guildid):
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
                guildobject = bot.get_guild(guildid)
                userobject = await guildobject.fetch_member(user)
                the_list += f'{str(x + 1)}. {userobject.mention} - **{msgs} messages **\n'
            except:
                pass
        return the_list
    except:
        return None

async def tmessageleaderboard(bot, guildid):
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
                guildobject = bot.get_guild(guildid)
                userobject = await guildobject.fetch_member(user)
                the_list += f'{str(x + 1)}. {userobject.mention} - **{msgs} messages **\n'
            except:
                pass
        return the_list
    except:
        return None

async def dmessageleaderboard(bot, guildid):
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
                guildobject = bot.get_guild(guildid)
                userobject = await guildobject.fetch_member(user)
                the_list += f'{str(x + 1)}. {userobject.mention} - **{msgs} messages **\n'
            except:
                pass
        return the_list
    except:
        return None

async def vcleaderboard(bot, guildid):
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
                guildobject = bot.get_guild(guildid)
                userobject = await guildobject.fetch_member(user)
                the_vclist += f'{str(x + 1)}. {userobject.mention} - **{vchours} hours and {vc} minutes **\n'
            except:
                pass

        return the_vclist
    except:
        return None

async def tvcleaderboard(bot, guildid):
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
                guildobject = bot.get_guild(guildid)
                userobject = await guildobject.fetch_member(user)
                the_vclist += f'{str(x + 1)}. {userobject.mention} - **{vchours} hours and {vc} minutes **\n'
            except:
                pass
        return the_vclist
    except:
        return None

async def dvcleaderboard(bot, guildid):
    conn, c = connect(guildid)
    try:
        c.execute('SELECT userid FROM dvcTime ORDER BY dvc DESC')
        all_user = c.fetchall()
        c.execute('SELECT dvc FROM dvcTime ORDER BY dvc DESC')
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
                guildobject = bot.get_guild(guildid)
                userobject = await guildobject.fetch_member(user)
                the_vclist += f'{str(x + 1)}. {userobject.mention} - **{vchours} hours and {vc} minutes **\n'
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
        c.execute("SELECT dvc from dvcTime WHERE userid = ?", (userid,))
        dvcount = c.fetchone()

        if vcount is None:
            vcount = 0

        if tvcount is None:
            tvcount = 0

        if dvcount is None:
            dvcount = 0

        uvctime = int(sqlTOstr(vcount))
        tuvctime = int(sqlTOstr(tvcount))
        duvctime = int(sqlTOstr(dvcount))
        userhours = 0
        tuserhours = 0
        duserhours = 0

        while uvctime > 60:
            userhours += 1
            uvctime -= 60

        while tuvctime > 60:
            tuserhours += 1
            tuvctime -= 60
        
        while duvctime > 60:
            duserhours += 1
            duvctime -= 60

        return userhours, uvctime, tuserhours, tuvctime, duserhours, duvctime
    except:
        return None

def glb_messagecount(guildid):
    conn, c = glb_connect()
    try:
        c.execute("SELECT msgs FROM guildmsgcount WHERE guildid = ?", (guildid,))
        count = c.fetchone()
        c.execute("SELECT tmsgs FROM tguildmsgcount WHERE guildid = ?", (guildid,))
        tcount = c.fetchone()
        c.execute("SELECT dmsgs FROM dguildmsgcount WHERE guildid = ?", (guildid,))
        dcount = c.fetchone()

        if count is None:
            count = 0
        if tcount is None:
            tcount = 0
        if dcount is None:
            dcount = 0

        msgcount = sqlTOstr(count)
        tmsgcount = sqlTOstr(tcount)
        dmsgcount = sqlTOstr(dcount)
        return msgcount, tmsgcount, dmsgcount
    except:
        return None

async def glb_messageleaderboard(bot):
    conn, c = glb_connect()
    try:
        c.execute('SELECT guildid FROM guildmsgcount ORDER BY msgs DESC')
        all_guild = c.fetchall()
        c.execute('SELECT msgs FROM guildmsgcount ORDER BY msgs DESC')
        all_msgs = c.fetchall()

        if len(all_guild) < 10:
            listrange = len(all_guild)
        else:
            listrange = 10
        
        the_list = ''
        for x in range(listrange):
            guild = sqlTOstr(all_guild[x])
            msgs = sqlTOstr(all_msgs[x])
            c.execute("SELECT code FROM invitecode WHERE guildid = ?", (guild,))
            code = c.fetchone()
            invitecode = sqlTOstr(code)
            if (invitecode != "None"):
                invitecode = "https://discord.gg/" + invitecode
            try:
                guildobject = bot.get_guild(int(guild))
                the_list += f'{str(x + 1)}. {guildobject.name} - **{msgs} messages ** [ invite: {invitecode} ]\n'
            except:
                pass
        return the_list
    except:
        return None

async def glb_tmessageleaderboard(bot):
    conn, c = glb_connect()
    try:
        c.execute('SELECT guildid FROM tguildmsgcount ORDER BY tmsgs DESC')
        all_guild = c.fetchall()
        c.execute('SELECT tmsgs FROM tguildmsgcount ORDER BY tmsgs DESC')
        all_msgs = c.fetchall()

        if len(all_guild) < 10:
            listrange = len(all_guild)
        else:
            listrange = 10
            
        the_list = ''
        for x in range(listrange):
            guild = sqlTOstr(all_guild[x])
            msgs = sqlTOstr(all_msgs[x])
            c.execute("SELECT code FROM invitecode WHERE guildid = ?", (guild,))
            code = c.fetchone()
            invitecode = sqlTOstr(code)
            if (invitecode != "None"):
                invitecode = "https://discord.gg/" + invitecode
            try:
                guildobject = bot.get_guild(int(guild))
                the_list += f'{str(x + 1)}. {guildobject.name} - **{msgs} messages ** [ invite: {invitecode} ]\n'
            except:
                pass
        return the_list
    except:
        return None

async def glb_dmessageleaderboard(bot):
    conn, c = glb_connect()
    try:
        c.execute('SELECT guildid FROM dguildmsgcount ORDER BY dmsgs DESC')
        all_guild = c.fetchall()
        c.execute('SELECT dmsgs FROM dguildmsgcount ORDER BY dmsgs DESC')
        all_msgs = c.fetchall()

        if len(all_guild) < 10:
            listrange = len(all_guild)
        else:
            listrange = 10
            
        the_list = ''
        for x in range(listrange):
            guild = sqlTOstr(all_guild[x])
            msgs = sqlTOstr(all_msgs[x])
            c.execute("SELECT code FROM invitecode WHERE guildid = ?", (guild,))
            code = c.fetchone()
            invitecode = sqlTOstr(code)
            if (invitecode != "None"):
                invitecode = "https://discord.gg/" + invitecode
            try:
                guildobject = bot.get_guild(int(guild))
                the_list += f'{str(x + 1)}. {guildobject.name} - **{msgs} messages ** [ invite: {invitecode} ]\n'
            except:
                pass
        return the_list
    except:
        return None

async def glb_vcleaderboard(bot):
    conn, c = glb_connect()
    try:
        c.execute('SELECT guildid FROM guildvctime ORDER BY vc DESC')
        all_guild = c.fetchall()
        c.execute('SELECT vc FROM guildvctime ORDER BY vc DESC')
        all_vc = c.fetchall()

        if len(all_guild) < 10:
            listrange = len(all_guild)
        else:
            listrange = 10

        the_vclist = ''
        for x in range(listrange):
            guild = sqlTOstr(all_guild[x])
            vc = sqlTOstr(all_vc[x])
            vc = int(vc)
            vchours = 0

            while vc > 60:
                vchours += 1
                vc -= 60

            try:
                guildobject = bot.get_guild(int(guild))
                the_vclist += f'{str(x + 1)}. {guildobject.name} - **{vchours} hours and {vc} minutes **\n'
            except:
                pass

        return the_vclist
    except:
        return None

async def glb_tvcleaderboard(bot):
    conn, c = glb_connect()
    c.execute('SELECT guildid FROM tguildvctime ORDER BY tvc DESC')
    all_guild = c.fetchall()
    c.execute('SELECT tvc FROM tguildvctime ORDER BY tvc DESC')
    all_vc = c.fetchall()

    if len(all_guild) < 10:
        listrange = len(all_guild)
    else:
        listrange = 10

    the_vclist = ''
    for x in range(listrange):
        guild = sqlTOstr(all_guild[x])
        vc = sqlTOstr(all_vc[x])
        vc = int(vc)
        vchours = 0

        while vc > 60:
            vchours += 1
            vc -= 60

        try:
            guildobject = bot.get_guild(int(guild))
            the_vclist += f'{str(x + 1)}. {guildobject.name} - **{vchours} hours and {vc} minutes **\n'
        except:
            pass
    return the_vclist

async def glb_dvcleaderboard(bot):
    conn, c = glb_connect()
    c.execute('SELECT guildid FROM dguildvctime ORDER BY dvc DESC')
    all_guild = c.fetchall()
    c.execute('SELECT dvc FROM dguildvctime ORDER BY dvc DESC')
    all_vc = c.fetchall()

    if len(all_guild) < 10:
        listrange = len(all_guild)
    else:
        listrange = 10

    the_vclist = ''
    for x in range(listrange):
        guild = sqlTOstr(all_guild[x])
        vc = sqlTOstr(all_vc[x])
        vc = int(vc)
        vchours = 0

        while vc > 60:
            vchours += 1
            vc -= 60

        try:
            guildobject = bot.get_guild(int(guild))
            the_vclist += f'{str(x + 1)}. {guildobject.name} - **{vchours} hours and {vc} minutes **\n'
        except:
            pass
    return the_vclist
    
def glb_vcount(guildid):
    conn, c = glb_connect()
    try:
        c.execute("SELECT vc FROM guildvctime WHERE guildid = ?", (guildid,))
        vcount = c.fetchone()
        c.execute("SELECT tvc from tguildvctime WHERE guildid = ?", (guildid,))
        tvcount = c.fetchone()
        c.execute("SELECT dvc from dguildvctime WHERE guildid = ?", (guildid,))
        dvcount = c.fetchone()

        if vcount is None:
            vcount = 0

        if tvcount is None:
            tvcount = 0

        if dvcount is None:
            dvcount = 0

        uvctime = int(sqlTOstr(vcount))
        tuvctime = int(sqlTOstr(tvcount))
        duvctime = int(sqlTOstr(dvcount))
        userhours = 0
        tuserhours = 0
        duserhours = 0

        while uvctime > 60:
            userhours += 1
            uvctime -= 60

        while tuvctime > 60:
            tuserhours += 1
            tuvctime -= 60
        
        while duvctime > 60:
            duserhours += 1
            duvctime -= 60

        return userhours, uvctime, tuserhours, tuvctime, duserhours, duvctime
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

async def balleaderboard(bot, guildid):
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
                guildobject = bot.get_guild(guildid)
                userobject = await guildobject.fetch_member(user)
                the_list += f'{str(x + 1)}. {userobject.mention} - **${bals}**\n'
            except:
                pass
        return the_list
    except:
        return None

def resetlb():
    for filename in os.listdir(dbdir):
        if filename != f"guildmessages.db":
            conn = sqlite3.connect(f"{dbdir}{filename}")
            c = conn.cursor()
            try:
                c.execute('UPDATE msgCount SET msgs = 0 WHERE msgs < 999999')
                c.execute('UPDATE vcTime SET vc = 0 WHERE vc < 999999')
                conn.commit()
                print(f"Leaderboard Reset Succeeded for {filename}")
            except:
                print(f"Leaderboard Reset Failed for {filename}")
    gconn, gc = glb_connect()
    try:
        gc.execute('UPDATE guildmsgcount SET msgs = 0 WHERE msgs < 999999')
        gc.execute('UPDATE guildvctime SET vc = 0 WHERE vc < 999999')
        gconn.commit()
        print(f"Leaderboard Reset Succeeded for guild leaderboards")
    except:
        print(f"Leaderboard Reset Failed for guild leaderboards")

def resetdlb():
    for filename in os.listdir(dbdir):
        if filename != f"guildmessages.db":
            conn = sqlite3.connect(f"{dbdir}{filename}")
            c = conn.cursor()
            try:
                c.execute('UPDATE dmsgCount SET dmsgs = 0 WHERE dmsgs < 999999')
                c.execute('UPDATE dvcTime SET dvc = 0 WHERE dvc < 999999')
                conn.commit()
                print(f"Leaderboard Reset Succeeded for {filename}")
            except:
                print(f"Leaderboard Reset Failed for {filename}")
    gconn, gc = glb_connect()
    try:
        gc.execute('UPDATE dguildmsgcount SET dmsgs = 0 WHERE dmsgs < 999999')
        gc.execute('UPDATE dguildvctime SET dvc = 0 WHERE dvc < 999999')
        gconn.commit()
        print(f"Leaderboard Reset Succeeded for guild leaderboards")
    except:
        print(f"Leaderboard Reset Failed for guild leaderboards")
            
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

def cleanTimeLog():
    for filename in os.listdir(dbdir):
        if filename != f"guildmessages.db":
            conn = sqlite3.connect(f"{dbdir}{filename}")
            c = conn.cursor()
            try:
                c.execute('DELETE FROM timeLog')
                conn.commit()
                print(f"Time Log Reset Succeeded for {filename}")
            except:
                print(f"Time Log Reset Failed for {filename}")

def newdbfile(guildid):
    filename = f"{dbdir}({guildid}) sql.db"
    open(filename)

def deletedbfile(guildid):
    filename = f"{dbdir}({guildid}) sql.db"
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        print(f"Error: {filename} file not found")