##-------------------------------------------------- IMPORTS ---------------------------------------------------##

import discord
from discord.ext import tasks
from discord.ext import commands

import lib.slash_util as slash_util
import lib.embed
import lib.economy
import lib.sql
import cogs.general

import time
import datetime
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True

extensions = ['cogs.general', 'cogs.leaderboards', 'cogs.info', 'cogs.econ', 'cogs.admin']
slashextensions = ['slashcogs.slashgeneral', 'slashcogs.slashleaderboards', 'slashcogs.slashinfo', 'slashcogs.slashecon', 'slashcogs.slashadmin']

class MyBot(slash_util.Bot):
    def __init__(self):
        super().__init__(command_prefix="eb ", case_insensitive=True, owner_id=329326685185114115, help_command=None, intents=intents)

        for ext in extensions:
            self.load_extension(ext)
            print(f"loaded cog: {ext}")

        for sext in slashextensions:
            self.load_extension(sext)
            print(f"loaded cog: {sext}")

bot = MyBot()

##-------------------------------------------------- DEFINITIONS ---------------------------------------------------##

def read_token():
    with open("ebykbottoken.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

##---------- Update Message -----------##
@commands.is_owner()
@bot.command()
async def updatemsg(ctx):
    guilds = len(bot.guilds)
    embed = lib.embed.systemEmbed(f"""~ **EbykBot V2.0 UPDATE ANNOUNCEMENT** ~\n\nThank you for using Ebyk Bot!\nI'm happy to say we have reached **~89 servers** and **~300,000 users**!\nI couldn't have done it without you guys\n\nEbykBot V2.0 has been released with changes according to discord's new API\n**PLEASE** feel free to add me at ebyk#1660 and message me with bugs or suggestions\n""", bot)
    embed.add_field(name="Change Log", value=f"""\n- reorganization of bot infrastructure using libraries and cogs\n- removal of snipe and esnipe commands due to message intent changes from discord\n- implementation of slash commands\n\n*Join the support server at: https://discord.gg/prcN3AtNcZ*""", inline=False)
    embed2 = lib.embed.systemEmbed(f"""~ **IMPORTANT** ~\n\nIn order to access **slash commands**, you need to re-invite the bot using this new invite link:\nhttps://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=277025508416&scope=bot%20applications.commands\n""", bot)
    failed = []
    
    for server in bot.guilds:
        try:
            member = discord.utils.get(server.members, id=server.owner_id)
            await member.send(content=None, embed=embed)
            await member.send(content=None, embed=embed2)
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
            await member.send(content=None, embed=embed2)
            print(f"message sent [{server.name}]")
            failed.remove(server)
            time.sleep(10)
        except:
            print(f"message FAILED [{server.name}]")
            pass
    
    print(f"\n\nTHIRD ATTEMPT\n\n")
    time.sleep(30)
    for server in failed:
        tchannel = None
        for tc in server.text_channels:
            state = False
            try:
                await tc.send(content=f"{member.mention}")
                state = True
                tchannel = tc
            except:
                pass
            if state == True:
                break
        try:
            member = discord.utils.get(server.members, id=server.owner_id)
            await tchannel.send(content="", embed=embed)
            await tchannel.send(content=None, embed=embed2)
            print(f"message sent [{server.name}] in ({tc.name})")
            failed.remove(server)
            time.sleep(10)
        except:
            print(f"message FAILED [{server.name}] in ({tc.name})")
            pass

    print(f"done with {len(failed)} fails")

##---------- Update Test -----------##
@commands.is_owner()
@bot.command()
async def updatemsgtest(ctx):
    guilds = len(bot.guilds)
    embed = lib.embed.systemEmbed(f"""~ **EbykBot V2.0 UPDATE ANNOUNCEMENT** ~\n\nThank you for using Ebyk Bot!\nI'm happy to say we have reached **~89 servers** and **~300,000 users**!\nI couldn't have done it without you guys\n\nEbykBot V2.0 has been released with changes according to discord's new API\n**PLEASE** feel free to add me at ebyk#1660 and message me with bugs or suggestions\n""", bot)
    embed.add_field(name="Change Log", value=f"""\n- reorganization of bot infrastructure using libraries and cogs\n- removal of snipe and esnipe commands due to message intent changes from discord\n- implementation of slash commands\n\n*Join the support server at: https://discord.gg/prcN3AtNcZ*""", inline=False)
    embed2 = lib.embed.systemEmbed(f"""~ **IMPORTANT** ~\n\nIn order to access **slash commands**, you need to re-invite the bot using this new invite link:\nhttps://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=277025508416&scope=bot%20applications.commands\n""", bot)
    await ctx.send(content=None, embed=embed)
    await ctx.send(content=None, embed=embed2)
    number = 0

@tasks.loop(hours=1.0)
async def updatestats():
    await bot.wait_until_ready()
    general.updatestatus()
    
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

updatestatus.start()
checkday.start()
resetdailylb.start()
        
if __name__ == '__main__':
    token = read_token()
    bot.run(token)
