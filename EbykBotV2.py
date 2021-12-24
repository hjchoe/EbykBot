##-------------------------------------------------- IMPORTS ---------------------------------------------------##

import discord
from discord.ext import tasks
from discord.ext import commands

import lib.slash_util as slash_util
import lib.embed
import lib.economy
import lib.sql

import time
import datetime
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True

extensions = ['cogs.general', 'cogs.leaderboards', 'cogs.info', 'cogs.econ', 'cogs.admin']
slashextensions = ['slashcogs.slashgeneral', 'slashcogs.slashleaderboards', 'slashcogs.slashinfo', 'slashcogs.slashecon']

class MyBot(slash_util.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", case_insensitive=True, owner_id=329326685185114115, help_command=None, intents=intents)

        for ext in extensions:
            self.load_extension(ext)

        for sext in slashextensions:
            self.load_extension(sext)

bot = MyBot()

##-------------------------------------------------- DEFINITIONS ---------------------------------------------------##

def read_token():
    with open("testtoken.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

##---------- Update Message -----------##
@commands.is_owner()
@bot.command()
async def updatemsg(ctx):
    guilds = len(bot.guilds)
    embed = lib.embed.systemEmbed(f"""~ **EbykBot V2.0 UPDATE ANNOUNCEMENT** ~\n\nThank you for using Ebyk Bot!\nI'm happy to say we have reached **~88 servers** and **~300,000 users**!\nI couldn't have done it without you guys\n\nEbykBot V2.0 has been released with changes according to discord's new API\n**PLEASE** feel free to add me at ebyk#1660 and message me with bugs or suggestions\n""", bot)
    embed.add_field(name="Change Log", value=f"""\n- reorganization of bot infrastructure using libraries and cogs\n- removal of snipe and esnipe commands due to message intent changes from discord\n- implementation of slash commands\n\n*Join the support server at: https://discord.gg/prcN3AtNcZ*""", inline=False)
    failed = []
    for server in bot.guilds:
        try:
            member = discord.utils.get(server.members, id=server.owner_id)
            await member.send(content=None, embed=embed)
            print(f"message sent [{server.name}]")
            time.sleep(1)
        except:
            print(f"message FAILED [{server.name}]")
            failed.append(server)
            pass
    

    print(f"\n\nSECOND ATTEMPT\n\n")
    time.sleep(30)
    for server in failed:
        try:
            member = discord.utils.get(server.members, id=server.owner_id)
            await member.send(content=None, embed=embed)
            print(f"message sent [{server.name}]")
            time.sleep(10)
        except:
            print(f"message FAILED [{server.name}]")
            pass


    print("done")

##---------- Update Test -----------##
@commands.is_owner()
@bot.command()
async def updatemsgtest(ctx):
    guilds = len(bot.guilds)
    embed = lib.embed.systemEmbed(f"""~ **EbykBot V2.0 UPDATE ANNOUNCEMENT** ~\n\nThank you for using Ebyk Bot!\nI'm happy to say we have reached **~88 servers** and **~300,000 users**!\nI couldn't have done it without you guys\n\nEbykBot V2.0 has been released with changes according to discord's new API\n**PLEASE** feel free to add me at ebyk#1660 and message me with bugs or suggestions\n""", bot)
    embed.add_field(name="Change Log", value=f"""\n- reorganization of bot infrastructure using libraries and cogs\n- removal of snipe and esnipe commands due to message intent changes from discord\n- implementation of slash commands\n\n*Join the support server at: https://discord.gg/prcN3AtNcZ*""", inline=False)
    await ctx.send(content=None, embed=embed)

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
    bot.run(token)

#token = read_token()
#bot.run(token)