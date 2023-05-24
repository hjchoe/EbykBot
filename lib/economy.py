import random
from . import sql

##---------- ECONOMY -----------##

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

def transaction(userid, guildid, win, betamt, bank):
    bank = int(bank)
    betamt = int(betamt)
    if win == True:
        bank += betamt
    else:
        bank -= betamt
    conn, c = sql.connect(guildid)
    try:
        c.execute('UPDATE bank SET money = ? WHERE userid = ?', (bank, userid))
        conn.commit()
    except:
        pass
    return bank

def givetransaction(userid, memberid, guildid, amount):
    ubank = sql.balancegrab(userid, guildid)
    rbank = sql.balancegrab(memberid, guildid)
    ubank = int(ubank)
    rbank = int(rbank)
    amount = int(amount)
    ubank -= amount
    rbank += amount
    conn, c = sql.connect(guildid)
    try:
        c.execute('UPDATE bank SET money = ? WHERE userid = ?', (ubank, userid))
        c.execute('UPDATE bank SET money = ? WHERE userid = ?', (rbank, memberid))
        conn.commit()
    except:
        pass