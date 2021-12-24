import discord

##---------- EMBED -----------##
def successEmbed(ctx, content, title):
    embed = discord.Embed(title='', description=content, color=3211008)
    embed.set_author(name=title, icon_url=ctx.author.avatar.url)
    return embed

def errorEmbed(ctx, content, title):
    embed = discord.Embed(title='', description=content, color=16711680)
    embed.set_author(name=title, icon_url=ctx.author.avatar.url)
    return embed

def systemEmbed(content, bot):
    embed = discord.Embed(title='', description=content, color=3037421)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
    return embed

def messageEmbed(ctx, userid, messages, tmessages, dmessages):
    embed = discord.Embed(title='', description=f"**Daily:** {dmessages} messages\n**Weekly:** {messages} messages\n**Total:** {tmessages} messages", color=16645526)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s # of messages""", icon_url=member.avatar.url)
    return embed

def vcEmbed(ctx, userid, hours, minutes, thours, tminutes):
    embed = discord.Embed(title='', description=f"**Weekly:** \n**{hours}** hours and **{minutes}** minutes \n\n**Total:** \n**{thours}** hours and **{tminutes}** minutes", color=16645526)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s vc time""", icon_url=member.avatar.url)
    return embed

def lbEmbed(ctx, title, lb):
    embed = discord.Embed(title='', description=lb, color=13276925)
    embed.set_author(name=f"""{ctx.guild.name}'s {title} Leaderboard""", icon_url=ctx.guild.icon.url)
    return embed

def balEmbed(ctx, userid, amt):
    embed = discord.Embed(title='', description=f"Balance: **${amt}**", color=16645526)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s Bank""", icon_url=member.avatar.url)
    return embed

def coinflipEmbed(ctx, userid, win, side, coin, betamt, amt):
    if win == True:
        color = 9498256
        win = "WON"
    else:
        color = 16619158
        win = "LOST"
    embed = discord.Embed(title='', description=f"**Guess:** {side}\n**Coin:** {coin}\n**Result:** {win}\n**Amount Bet:** ${betamt}\n**New Balance:** ${amt}", color=color)
    member = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""{member.name}'s Result""", icon_url=member.avatar.url)
    return embed

def giveEmbed(ctx, userid, memberid, amt):
    receiver = discord.utils.get(ctx.author.guild.members, id=memberid)
    embed = discord.Embed(title='', description=f"{ctx.author.mention} gave {receiver.mention} **${amt}**", color=16645526)
    giver = discord.utils.get(ctx.author.guild.members, id=userid)
    embed.set_author(name=f"""Money Transfer""", icon_url=giver.avatar.url)
    return embed