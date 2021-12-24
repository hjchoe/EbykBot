import discord
import lib.slash_util as slash_util

class MyCog(slash_util.ApplicationCog):
    @slash_util.slash_command(description="Shows the avatar of the user.")
    @slash_util.describe(user="The user you want avatar of.")
    async def avatar(self, ctx, user: discord.Member): 
        userave = discord.Embed(title='', description=f"""<@{user.id}>'s pfp""", color=16580705)
        userave.set_image(url=user.avatar.url)
        userave.set_footer(text=f"""requested by {user}""")
        await ctx.send(content=None, embed=userave)

def setup(bot):
    bot.add_cog(MyCog(bot))