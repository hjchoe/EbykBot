##-------------------------------------------------- IMPORTS ---------------------------------------------------##

import discord
from discord.ext import tasks
from discord.ext import commands

import lib.slash_util as slash_util
import lib.embed
import lib.economy
import lib.sql

import datetime
from multiprocessing import Process
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True

extensions = ['cogs.general', 'cogs.leaderboards', 'cogs.info', 'cogs.econ', 'cogs.admin']

class MyBot(slash_util.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", case_insensitive=True, owner_id=329326685185114115, help_command=None, intents=intents)

        for ext in extensions:
            self.load_extension(ext)

bot = MyBot()

##-------------------------------------------------- DEFINITIONS ---------------------------------------------------##

def read_token():
    with open("testtoken.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

@tasks.loop(hours=12.0)
async def checkday():
    await bot.wait_until_ready()
    day = datetime.datetime.today().strftime('%A')
    if day == "Sunday":
        lib.sql.resetlb()

@tasks.loop(hours=24.0)
async def resetdailylb():
    await bot.wait_until_ready()
    lib.sql.resetdlb()

checkday.start()
resetdailylb.start()
        
if __name__ == '__main__':
    token = read_token()
    MyBot().run(token)

#token = read_token()
#bot.run(token)