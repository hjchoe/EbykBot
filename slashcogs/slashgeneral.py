import discord
import lib.slash_util as slash_util

class MyCog(slash_util.ApplicationCog):

    @slash_util.slash_command(description="Shows the avatar of the user")
    @slash_util.describe(user="The user you want avatar of.")
    async def avatar(self, ctx, user: discord.Member): 
        user = user or ctx.author
        emb = discord.Embed(
                title=f"{user}'s avatar",
                color=discord.Color.blue()
            )
        emb.set_image(url=user.avatar.url)
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(MyCog(bot))