import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import lib.embed

class GeneralCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    ##---------- AVATAR -----------##
    @app_commands.command(name="avatar", description="Shows the avatar of the user.")
    @app_commands.describe(user="The user you want the avatar/pfp of.")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member=None) -> None: 
        try:
            userave = discord.Embed(title='', description=f"""<@{user.id}>'s pfp""", color=16580705)
            userave.set_image(url=user.avatar.url)
        except:
            userave = discord.Embed(title='', description=f"""<@{interaction.user.id}>'s pfp""", color=16580705)
            userave.set_image(url=interaction.user.avatar.url)
        userave.set_footer(text=f"""requested by {interaction.user}""")
        await interaction.response.send_message(content=None, embed=userave)

    ##---------- HELP ----------##
    @app_commands.command(name="help", description="Shows help menu.")
    @app_commands.describe(section="Section of help menu.")
    @app_commands.choices(section=[
        Choice(name="Help Menu Options", value=0),
        Choice(name="General Help", value=1),
        Choice(name="Leaderboard Help", value=2),
        Choice(name="Economy Help", value=3),
        Choice(name="Admin Help", value=4),
    ])
    async def help(self, interaction: discord.Interaction, section: int) -> None:
        helpe = discord.Embed(title='', description="prefix: /", color=3037421)
        helpe.set_author(name="Ebyk Bot Help Page", icon_url=self.bot.user.avatar.url)
        helpe.set_footer(text="Programmed by ebyk#1660, dm for questions.")
        if section == 0:
            helpe.add_field(name='/help [General Help]', value='open general commands help menu', inline=False)
            helpe.add_field(name='/help [Leaderboard Help]', value='open message/vc leaderboards help menu', inline=False)
            helpe.add_field(name='/help [Economy Help]', value='open economy help menu', inline=False)
            helpe.add_field(name='/help [Admin Help]', value='open admin help menu', inline=False)
        elif section == 1:
            helpe.add_field(name='/help', value='open help menu', inline=False)
            helpe.add_field(name='/test', value='test if the bot is online and get latency', inline=False)
            helpe.add_field(name='/avatar', value='check your pfp', inline=False)
            helpe.add_field(name='/invite', value="get bot's invite link", inline=False)
            helpe.add_field(name='/user info', value='get information about a user', inline=False)
            helpe.add_field(name='/server info', value='get information about a server', inline=False)
            helpe.add_field(name='/boosts', value='get server boost information', inline=False)
            helpe.add_field(name='/guilds', value='get bot guild information', inline=False)
        elif section == 2:
            helpe.add_field(name='/messages', value='check how many messages you sent', inline=False)
            helpe.add_field(name='/message leaderboard [Daily]', value='check the daily message leaderboard', inline=False)
            helpe.add_field(name='/message leaderboard [Weekly]', value='check the weekly message leaderboard', inline=False)
            helpe.add_field(name='/message leaderboard [Total]', value='check the total message leaderboard', inline=False)
            helpe.add_field(name='/vc', value='check how much time you spent in vc', inline=False)
            helpe.add_field(name='/vc leaderboard [Daily]', value='check the daily vc leaderboard', inline=False)
            helpe.add_field(name='/vc leaderboard [Weekly]', value='check the weekly vc leaderboard', inline=False)
            helpe.add_field(name='/vc leaderboard [Total]', value='check the total vc leaderboard', inline=False)
            helpe.add_field(name='/guild messages', value='check how many messages current server has sent', inline=False)
            helpe.add_field(name='/guild message leaderboard [Daily]', value='check the daily guild message leaderboard', inline=False)
            helpe.add_field(name='/guild message leaderboard [Weekly]', value='check the weekly guild message leaderboard', inline=False)
            helpe.add_field(name='/guild message leaderboard [Total]', value='check the total guild message leaderboard', inline=False)
            helpe.add_field(name='/guild vc', value='check how much time current server has spent in vc', inline=False)
            helpe.add_field(name='/guild vc leaderboard [Daily]', value='check the daily guild vc leaderboard', inline=False)
            helpe.add_field(name='/guild vc leaderboard [Weekly]', value='check the weekly guild vc leaderboard', inline=False)
            helpe.add_field(name='/guild vc leaderboard [Total]', value='check the total guild vc leaderboard', inline=False)
        elif section == 3:
            helpe.add_field(name='/balance', value='check your balance', inline=False)
            helpe.add_field(name='/balance leaderboard', value='check the server balance leaderboard', inline=False)
            helpe.add_field(name='/coin flip', value='bet and gamble your money on a coin flip', inline=False)
            helpe.add_field(name='/give', value='give somebody a certain amount from your bank', inline=False)
        elif section == 4:
            helpe.add_field(name='/reset total message leaderboard', value='reset the total leaderboard for messages, requires Admin Permission', inline=False)
            helpe.add_field(name='/reset total vc leaderboard', value='reset the total leaderboard for voice, requires Admin Permission', inline=False)        
            helpe.add_field(name='/remove messages', value='remove total messages from a member, requires Admin Permission', inline=False)
            helpe.add_field(name='/invite code', value='set the invite code for your server, requires Admin Permission', inline=False)

        helpe.set_footer(text="Join Support Server: https://discord.gg/prcN3AtNcZ")
        await interaction.response.send_message(content=None, embed=helpe)

    ##---------- INVITE -----------##
    @app_commands.command(name="invite", description="Provides invite link for bot.")
    async def invite(self, interaction: discord.Interaction) -> None:
        embed = lib.embed.systemEmbed('**Invite:** https://discord.com/api/oauth2/authorize?client_id=800171925275017237&permissions=277025508416&scope=bot%20applications.commands\nadd + dm **ebyk#1660** for questions or suggestions', self.bot)
        await interaction.response.send_message(content=None, embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCog(bot))