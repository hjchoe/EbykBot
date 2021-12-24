import discord
import slash_util

class MyCog(slash_util.ApplicationCog):
    @slash_util.slash_command()  # sample slash command
    async def slash(self, ctx: slash_util.Context, number: int):
        await ctx.send(f"You selected #{number}!", ephemeral=True)
    
    @slash_util.message_command(name="Quote")  # sample command for message context menus
    async def quote(self, ctx: slash_util.Context, message: discord.Message):  # these commands may only have a single Message parameter
        await ctx.send(f'> {message.clean_content}\n- {message.author}')
    
    @slash_util.user_command(name='Bonk')  # sample command for user context menus
    async def bonk(self, ctx: slash_util.Context, user: discord.Member):  # these commands may only have a single Member parameter
        await ctx.send(f'{ctx.author} BONKS {user} :hammer:')

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