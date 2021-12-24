import discord
import lib.slash_util as slash_util
import lib.embed

class sGeneralCog(slash_util.ApplicationCog):
    ##---------- Message Count ----------##
    @slash_util.slash_command(description="Shows the messages of a user.")
    @slash_util.describe(user="The user you want the message info of.")
    async def messages(self, ctx, member: discord.Member=None):
        if member == None:
            userid = ctx.author.id
        else:
            userid = member.id
        umsgcount, tmsgcount, dmsgcount = lib.sql.messagecount(userid, ctx.guild.id)

        embed = lib.embed.messageEmbed(ctx, userid, umsgcount, tmsgcount, dmsgcount)
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(sGeneralCog(bot))