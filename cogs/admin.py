import discord
from discord import app_commands
from discord.ext import commands
import lib.embed
import lib.sql

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    ##---------- Admin Total Message LB Reset -----------##
    @app_commands.command(name="reset_total_message_leaderboard", description="[ADMIN] Reset total message leaderboard.")
    async def reset_total_mlb(self, interaction: discord.Interaction) -> None:
        if (interaction.permissions.administrator):
            lib.sql.resettmlb(interaction.guild_id)
            embed = lib.embed.systemEmbed("Finished manual reset of total message leaderboard", self.bot)
        else:
            embed = lib.embed.errorEmbed(interaction, "Failed to reset total message leaderboard", "Missing Admin Permissions")
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Admin Total Voice LB Reset -----------##
    @app_commands.command(name="reset_total_vc_leaderboard", description="[ADMIN] Reset total voice leaderboard.")
    async def reset_total_vclb(self, interaction: discord.Interaction) -> None:
        if (interaction.permissions.administrator):
            lib.sql.resettvclb(interaction.guild.id)
            embed = lib.embed.systemEmbed("Finished manual reset of total voice leaderboard", self.bot)
        else:
            embed = lib.embed.errorEmbed(interaction, "Failed to reset total voice leaderboard", "Missing Admin Permissions")
        await interaction.respone.send_message(content=None, embed=embed)
            
    ##---------- Admin Message Remove -----------##
    @app_commands.command(name="remove_messages", description="[ADMIN] Remove a certain amount of messages from a user.")
    @app_commands.describe(user="The user you want to remove messages from.", messages="The number of messages to remove.")
    async def removemessages(self, interaction: discord.Interaction, user: discord.Member, messages: int) -> None:
        if (interaction.permissions.administrator):
            conn, c = lib.sql.connect(interaction.guild.id)
            c.execute("SELECT tmsgs from totalmsgCount WHERE userid = ?", (user.id,))
            tcount = c.fetchone()
            if int(messages) > int(tcount[0]):
                newtcount = 0
                c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (newtcount, user.id))
                conn.commit()
            else:
                newtcount = int(tcount[0])-int(messages)
                c.execute('UPDATE totalmsgCount SET tmsgs = ? WHERE userid = ?', (newtcount, user.id))
                conn.commit()
            embed = lib.embed.systemEmbed(f"Removed {messages} messages from {user.mention}. They are now at {newtcount} messages.", self.bot)
        else:
            embed = lib.embed.errorEmbed(interaction, f"Failed to remove {messages} messages from {user.mention}", "Missing Admin Permissions")
        await interaction.response.send_message(content=None, embed=embed)

    ##---------- Set Invite Code -----------##
    @app_commands.command(name="invite_code", description="[ADMIN] Set the invite code for your server to show up in guild leaderboards.")
    @app_commands.describe(code="The invite code you want to set for your server.")
    async def invitecode(self, interactions: discord.Interaction, code: str) -> None:
        conn, c = lib.sql.glb_connect()

        c.execute("SELECT code from invitecode WHERE guildid = ?", (interactions.guild.id,))
        invcode = c.fetchone()

        code = code.replace("https://discord.gg/",'')

        if invcode is None:
            c.execute('INSERT INTO invitecode (guildid, code) VALUES (?,?)', (interactions.guild.id, code))
            conn.commit()
        else:
            c.execute('UPDATE invitecode SET code = ? WHERE guildid = ?', (code, interactions.guild.id))
            conn.commit()

        embed = lib.embed.systemEmbed(f"Set {interactions.guild.name}'s invite to: https://discord.gg/{code}.", self.bot)
        await interactions.response.send_message(content=None, embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))
