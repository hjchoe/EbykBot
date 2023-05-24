import discord

##---------- EMBED -----------##
def successEmbed(interaction: discord.Interaction, content, title):
    embed = discord.Embed(title='', description=content, color=3211008)
    embed.set_author(name=title, icon_url=interaction.author.avatar.url)
    return embed

def errorEmbed(interaction: discord.Interaction, content, title):
    embed = discord.Embed(title='', description=content, color=16711680)
    embed.set_author(name=title, icon_url=interaction.author.avatar.url)
    return embed

def systemEmbed(content, bot):
    embed = discord.Embed(title='', description=content, color=3037421)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
    return embed

async def messageEmbed(interaction: discord.Interaction, userid, messages, tmessages, dmessages):
    embed = discord.Embed(title='', description=f"**Daily:** {dmessages} messages\n**Weekly:** {messages} messages\n**Total:** {tmessages} messages", color=16645526)
    # member = discord.utils.get(ctx.author.guild.members, id=userid)
    member = await interaction.guild.fetch_member(userid)
    embed.set_author(name=f"""{member.name}'s # of messages""", icon_url=member.avatar.url)
    return embed

def glb_messageEmbed(interaction: discord.Interaction, bot, messages, tmessages, dmessages):
    embed = discord.Embed(title='', description=f"**Daily:** {dmessages} messages\n**Weekly:** {messages} messages\n**Total:** {tmessages} messages", color=16645526)
    guild = bot.get_guild(interaction.guild.id)
    embed.set_author(name=f"""{guild.name}'s # of messages""", icon_url=guild.icon.url)
    return embed

async def vcEmbed(interaction: discord.Interaction, userid, hours, minutes, thours, tminutes, dhours, dminutes):
    embed = discord.Embed(title='', description=f"**Daily:** \n**{dhours}** hours and **{dminutes}** \n\n**Weekly:** \n**{hours}** hours and **{minutes}** minutes \n\n**Total:** \n**{thours}** hours and **{tminutes}** minutes", color=16645526)
    # member = discord.utils.get(ctx.author.guild.members, id=userid)
    member = await interaction.guild.fetch_member(userid)
    embed.set_author(name=f"""{member.name}'s vc time""", icon_url=member.avatar.url)
    return embed

def glb_vcEmbed(interaction: discord.Interaction, bot, hours, minutes, thours, tminutes, dhours, dminutes):
    embed = discord.Embed(title='', description=f"**Daily:** \n**{dhours}** hours and **{dminutes}** \n\n**Weekly:** \n**{hours}** hours and **{minutes}** minutes \n\n**Total:** \n**{thours}** hours and **{tminutes}** minutes", color=16645526)
    guild = bot.get_guild(interaction.guild.id)
    embed.set_author(name=f"""{guild.name}'s vc time""", icon_url=guild.icon.url)
    return embed

def lbEmbed(interaction: discord.Interaction, title, lb):
    embed = discord.Embed(title='', description=lb, color=13276925)
    embed.set_author(name=f"""{interaction.guild.name}'s {title} Leaderboard""", icon_url=interaction.guild.icon.url)
    return embed

def glb_lbEmbed(interaction: discord.Interaction, title, lb):
    embed = discord.Embed(title='', description=lb, color=16765404)
    embed.set_author(name=f"""{title} Guild Leaderboard""", icon_url=interaction.guild.icon.url)
    embed.set_footer(text="SERVER ADMINS: run the invitecode command to add an invite code to your server.")
    return embed

async def balEmbed(interaction: discord.Interaction, userid, amt):
    embed = discord.Embed(title='', description=f"Balance: **${amt}**", color=16645526)
    # member = discord.utils.get(ctx.author.guild.members, id=userid)
    member = await interaction.guild.fetch_member(userid)
    embed.set_author(name=f"""{member.name}'s Bank""", icon_url=member.avatar.url)
    return embed

def coinflipEmbed(interaction: discord.Interaction, userid, win, side, coin, betamt, amt):
    if win == True:
        color = 9498256
        win = "WON"
    else:
        color = 16619158
        win = "LOST"
    embed = discord.Embed(title='', description=f"**Guess:** {side}\n**Coin:** {coin}\n**Result:** {win}\n**Amount Bet:** ${betamt}\n**New Balance:** ${amt}", color=color)
    member = discord.utils.get(interaction.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s Result""", icon_url=member.avatar.url)
    return embed

def giveEmbed(interaction: discord.Interaction, userid, memberid, amt):
    receiver = discord.utils.get(interaction.author.guild.members, id=memberid)
    embed = discord.Embed(title='', description=f"{interaction.author.mention} gave {receiver.mention} **${amt}**", color=16645526)
    giver = discord.utils.get(interaction.author.guild.members, id=userid)
    embed.set_author(name=f"""Money Transfer""", icon_url=giver.avatar.url)
    return embed