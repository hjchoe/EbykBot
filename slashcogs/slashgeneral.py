import discord
import lib.slash_util as slash_util
import lib.embed

class sGeneralCog(slash_util.ApplicationCog):
    ##---------- TEST -----------##
    @slash_util.slash_command(description="Test command with latency.")
    async def test(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = lib.embed.systemEmbed(f"""responding!\n\n**Ping: **{latency}ms""", self.bot)
        await ctx.send(content=None, embed=embed)

    ##---------- AVATAR -----------##
    @slash_util.slash_command(description="Shows the avatar of the user.")
    @slash_util.describe(user="The user you want avatar of.")
    async def avatar(self, ctx, user: discord.Member=None): 
        try:
            userave = discord.Embed(title='', description=f"""<@{user.id}>'s pfp""", color=16580705)
            userave.set_image(url=user.avatar.url)
        except:
            userave = discord.Embed(title='', description=f"""<@{ctx.author.id}>'s pfp""", color=16580705)
            userave.set_image(url=ctx.author.avatar.url)
        userave.set_footer(text=f"""requested by {ctx.author}""")
        await ctx.send(content=None, embed=userave)

    ##---------- HELP ----------##
    @slash_util.slash_command(description="Shows help menu.")
    @slash_util.describe(htype="Section of help menu (type nothing for menu of sections).")
    async def help(self, ctx, htype: str=None):
        helpe = discord.Embed(title='', description="prefix: eb ___", color=3037421)
        helpe.set_author(name="Ebyk Bot Help Page", icon_url=self.bot.user.avatar.url)
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

    ##---------- INVITE -----------##
    @slash_util.slash_command(description="Provides invite link for bot.")
    async def invite(self, ctx):
        embed = lib.embed.systemEmbed('**Invite:** https://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=650304&scope=bot\nadd + dm **ebyk#1660** for questions or suggestions', self.bot)
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(sGeneralCog(bot))