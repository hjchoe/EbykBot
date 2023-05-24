import discord
from discord import app_commands
from discord.ext import commands
import lib.embed
import lib.sql

class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    ##---------- TEST -----------##
    @app_commands.command(name="test", description="Test command with bot latency.")
    async def test(self, interaction: discord.Interaction) -> None:
        latency = round(self.bot.latency * 1000)
        embed = lib.embed.systemEmbed(f"""responding!\n\n**Ping: **{latency}ms""", self.bot)
        await interaction.response.send_message(content=None, embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TestCog(bot))