##-------------------------------------------------- IMPORTS ---------------------------------------------------##

import discord
from discord.ext import tasks
from discord.ext import commands

import lib.embed
import lib.economy
import lib.sql
import cogs.general

import asyncio
import time
import datetime

intents = discord.Intents.default()
intents.messages = False
intents.members = False
intents.presences = False

extensions = ['cogs.general', 'cogs.leaderboards', 'cogs.info', 'cogs.econ', 'cogs.admin']
slashextensions = ['slashcogs.slashgeneral', 'slashcogs.slashleaderboards', 'slashcogs.slashinfo', 'slashcogs.slashecon', 'slashcogs.slashadmin']

class MyBot(commands.Bot):
    async def setup_hook(self):
        super().__init__(command_prefix="eb ", case_insensitive=True, owner_id=329326685185114115, help_command=None, intents=intents)

        for ext in extensions:
            await self.load_extension(ext)
            print(f"loaded cog: {ext}")

        for sext in slashextensions:
            await self.load_extension(sext)
            print(f"loaded cog: {sext}")

bot = MyBot("eb ")

##-------------------------------------------------- DEFINITIONS ---------------------------------------------------##

tokenpath = "ebykbottoken.txt"
testtokenpath = "ebyktest.txt"

def read_token():
    with open(testtokenpath, "r") as f:
        lines = f.readlines()
        return lines[0].strip()

##---------- Update Message -----------##
@commands.is_owner()
@bot.command()
async def updatemsg(ctx):
    embed = lib.embed.systemEmbed(f"""~ **EbykBot V3.0 UPDATE ANNOUNCEMENT** ~\n\nThank you for using Ebyk Bot!\nWe've grown to **~142 servers** and **~800,000+ users**!\nEbyk Bot was also officially **verified** by Discord\nThis could not have been done without your continued support\n\nEbykBot V3.0 has been released with new features and changes according to discord's new API\n**PLEASE** feel free to add me at ebyk#1660 and message me with bugs or suggestions\n""", bot)
    embed.add_field(name="Change Log", value=f"""\n- addition of discord wide guild message and vc time leaderboards where servers are ranked based on their total messages sent and time spent in vc\n(server owners have the option to set an invite code to show up on the leaderboard as well)\nrun `eb h general` to check out new commands\n- bug fixes\n\n*Join the support server at: https://discord.gg/prcN3AtNcZ*""", inline=False)
    embed2 = lib.embed.systemEmbed(f"""~ **IMPORTANT** ~\n\nIn order to access **slash commands**, you need to re-invite the bot using this new invite link:\nhttps://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=277025508416&scope=bot%20applications.commands\n""", bot)
    failed = []
    
    for server in bot.guilds:
        print(server.owner_id)
        try:
            member = await server.fetch_member(server.owner_id)
            await member.send(content=None, embed=embed)
            await member.send(content=None, embed=embed2)
            print(f"message sent [{server.name}]")
            time.sleep(1)
        except:
            print(f"message FAILED [{server.name}]")
            failed.append(server)
    

    print(f"\n\nSECOND ATTEMPT\n\n")
    time.sleep(30)
    for server in failed:
        try:
            member = await server.fetch_member(server.owner_id)
            await member.send(content=None, embed=embed)
            await member.send(content=None, embed=embed2)
            print(f"message sent [{server.name}]")
            failed.remove(server)
            time.sleep(10)
        except:
            print(f"message FAILED [{server.name}]")
    
    print(f"\n\nTHIRD ATTEMPT\n\n")
    time.sleep(30)
    for server in failed:
        tchannel = None
        for tc in server.text_channels:
            state = False
            try:
                member = await server.fetch_member(server.owner_id)
                await tc.send(content=f"{member.mention}")
                state = True
                tchannel = tc
            except:
                pass
            if state == True:
                break
        try:
            member = await server.fetch_member(server.owner_id)
            await tchannel.send(content="", embed=embed)
            await tchannel.send(content=None, embed=embed2)
            print(f"message sent [{server.name}] in ({tc.name})")
            failed.remove(server)
            time.sleep(10)
        except:
            print(f"message FAILED [{server.name}] in ({tc.name})")

    print(f"done with {len(failed)} fails")

##---------- Update Test -----------##
@commands.is_owner()
@bot.command()
async def updatemsgtest(ctx):
    embed = lib.embed.systemEmbed(f"""~ **EbykBot V3.0 UPDATE ANNOUNCEMENT** ~\n\nThank you for using Ebyk Bot!\nWe've grown to **~142 servers** and **~800,000+ users**!\nEbyk Bot was also officially **verified** by Discord\nThis could not have been done without your continued support\n\nEbykBot V3.0 has been released with new features and changes according to discord's new API\n**PLEASE** feel free to add me at ebyk#1660 and message me with bugs or suggestions\n""", bot)
    embed.add_field(name="Change Log", value=f"""\n- addition of discord wide guild message and vc time leaderboards where servers are ranked based on their total messages sent and time spent in vc\n(server owners have the option to set an invite code to show up on the leaderboard as well)\nrun `eb h general` to check out new commands\n- bug fixes\n\n*Join the support server at: https://discord.gg/prcN3AtNcZ*""", inline=False)
    embed2 = lib.embed.systemEmbed(f"""~ **IMPORTANT** ~\n\nIn order to access **slash commands**, you need to re-invite the bot using this new invite link:\nhttps://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=277025508416&scope=bot%20applications.commands\n""", bot)
    await ctx.send(content=None, embed=embed)
    await ctx.send(content=None, embed=embed2)

@tasks.loop(hours=1.0)
async def updatestats():
    await bot.wait_until_ready()
    await cogs.general.updatestatus(bot)

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

updatestats.start()
checkday.start()
resetdailylb.start()
       
async def main():
    token = read_token()
    lib.sql.cleanTimeLog()
    await bot.start(token)

asyncio.run(main())
