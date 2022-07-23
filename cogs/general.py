import discord
from discord.ext import commands
import lib.embed
import lib.sql

async def updatestatus(bot):
    """
    totalusers = 0
    for server in bot.guilds:
        totalusers += len(server.members)
    """
    servermemcount = len(bot.guilds)
    
    activity = discord.Game(name=f"{servermemcount} servers | eb h for help")
    await bot.change_presence(status=discord.Status.online, activity=activity)

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##---------- TEST -----------##
    @commands.guild_only()
    @commands.command()
    async def test(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = lib.embed.systemEmbed(f"""responding!\n\n**Ping: **{latency}ms""", self.bot)
        await ctx.send(content=None, embed=embed)

    ##---------- AVATAR -----------##
    @commands.guild_only()
    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member : discord.Member=None):
        try:
            userave = discord.Embed(title='', description=f"""<@{member.id}>'s pfp""", color=16580705)
            userave.set_image(url=member.avatar.url)
        except:
            userave = discord.Embed(title='', description=f"""<@{ctx.author.id}>'s pfp""", color=16580705)
            userave.set_image(url=ctx.author.avatar.url)
        userave.set_footer(text=f"""requested by {ctx.author}""")
        await ctx.send(content=None, embed=userave)

    ##---------- HELP ----------##
    @commands.command(aliases=['h'])
    async def help(self, ctx, htype=None):
        helpe = discord.Embed(title='', description="prefix: eb ___", color=3037421)
        helpe.set_author(name="Ebyk Bot Help Page", icon_url=self.bot.user.avatar.url)
        helpe.set_footer(text="Programmed by ebyk#1660, dm for questions.")
        if htype == None:
            helpe.add_field(name='eb h general', value='open general commands help menu', inline=False)
            helpe.add_field(name='eb h leaderboards', value='open message/vc leaderboards help menu', inline=False)
            helpe.add_field(name='eb h economy', value='open economy help menu', inline=False)
            helpe.add_field(name='eb h admin', value='open admin help menu', inline=False)
        elif htype == "general":
            helpe.add_field(name='eb help (eb h)', value='open help menu', inline=False)
            helpe.add_field(name='eb test', value='test if the bot is online and get latency', inline=False)
            helpe.add_field(name='eb avatar (eb av)', value='check your pfp', inline=False)
            helpe.add_field(name='eb invite', value="get bot's invite link", inline=False)
            helpe.add_field(name='eb userinfo (eb whois)', value='get information about a user', inline=False)
            helpe.add_field(name='eb serverinfo (eb sf)', value='get information about a server', inline=False)
            helpe.add_field(name='eb boosts', value='get server boost information', inline=False)
            helpe.add_field(name='eb guilds', value='get bot guild information', inline=False)
        elif htype == "leaderboards":
            helpe.add_field(name='eb messages (eb m, eb msg)', value='check how many messages you sent', inline=False)
            helpe.add_field(name='eb mleaderboard (eb mlb)', value='check the weekly message leaderboard', inline=False)
            helpe.add_field(name='eb tmleaderboard (eb tmlb)', value='check the total message leaderboard', inline=False)
            helpe.add_field(name='eb dmleaderboard (eb dmlb)', value='check the daily message leaderboard', inline=False)
            helpe.add_field(name='eb vc', value='check how much time you spent in vc', inline=False)
            helpe.add_field(name='eb vcleaderboard (eb vclb)', value='check the weekly vc leaderboard', inline=False)
            helpe.add_field(name='eb tvcleaderboard (eb tvclb)', value='check the total vc leaderboard', inline=False)

            helpe.add_field(name='eb guildmessages (eb gm, eb guildmsg)', value='check how many messages current server has sent', inline=False)
            helpe.add_field(name='eb guildmleaderboard (eb gmlb)', value='check the weekly guild message leaderboard', inline=False)
            helpe.add_field(name='eb guildtmleaderboard (eb gtmlb)', value='check the total guild message leaderboard', inline=False)
            helpe.add_field(name='eb guilddmleaderboard (eb gdmlb)', value='check the daily guild message leaderboard', inline=False)
            helpe.add_field(name='eb gvc', value='check how much time current server has spent in vc', inline=False)
            helpe.add_field(name='eb guildvcleaderboard (eb gvclb)', value='check the weekly guild vc leaderboard', inline=False)
            helpe.add_field(name='eb guildtvcleaderboard (eb gtvclb)', value='check the total guild vc leaderboard', inline=False)
        elif htype == "economy":
            helpe.add_field(name='eb balance (eb b, eb bal)', value='check your balance', inline=False)
            helpe.add_field(name='eb bleaderboard (eb blb)', value='check the server balance leaderboard', inline=False)
            helpe.add_field(name='eb coinflip (eb cf)', value='bet and gamble your money on a coin flip', inline=False)
            helpe.add_field(name='eb give (eb g)', value='give somebody a certain amount from your bank', inline=False)
        elif htype == "admin":
            helpe.add_field(name='eb reset_total_mlb (eb rtmlb)', value='reset the total leaderboard for messages, requires Admin Permission', inline=False)
            helpe.add_field(name='eb reset_total_vclb (eb rtvclb)', value='reset the total leaderboard for voice, requires Admin Permission', inline=False)        
            helpe.add_field(name='eb removemessages (eb rm)', value='remove total messages from a member, requires Admin Permission', inline=False)
            helpe.add_field(name='eb invitecode (eb ic)', value='set the invite code for your server, requires Admin Permission', inline=False)

        helpe.set_footer(text="Join Support Server: https://discord.gg/prcN3AtNcZ")
        await ctx.channel.send(content=None, embed=helpe)

    ##---------- INVITE -----------##
    @commands.guild_only()
    @commands.command()
    async def invite(self, ctx):
        embed = lib.embed.systemEmbed('**Invite:** https://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=277025508416&scope=bot%20applications.commands\nadd + dm **ebyk#1660** for questions or suggestions', self.bot)
        await ctx.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            conn, c = lib.sql.connect(guild.id)

            c.execute('CREATE TABLE IF NOT EXISTS msgCount(userid VARCHAR(255), msgs INT)')
            c.execute('CREATE TABLE IF NOT EXISTS totalmsgCount(userid VARCHAR(255), tmsgs INT)')
            c.execute('CREATE TABLE IF NOT EXISTS vcTime(userid VARCHAR(255), vc INT)')
            c.execute('CREATE TABLE IF NOT EXISTS "totalvcTime"("userid" VARCHAR(255), "tvc" INT)')
            c.execute('CREATE TABLE IF NOT EXISTS timeLog(userid VARCHAR(255), jTime DATETIME)')
            c.execute('CREATE TABLE IF NOT EXISTS partnerCount(userid VARCHAR(255), partners INT)')
            c.execute('CREATE TABLE IF NOT EXISTS bank(userid VARCHAR(255), money INT)')
            conn.commit()
        except:
            lib.sql.newdbfile(guild.id)
        await updatestatus(self.bot)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await updatestatus(self.bot)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has connected to discord')
        await updatestatus(self.bot)

def setup(bot):
    bot.add_cog(GeneralCog(bot))
