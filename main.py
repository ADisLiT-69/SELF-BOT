import json
import os
import sys
import discord
from discord.enums import Status
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

PREFIX = config["prefix"]
TOKEN = config["token"]
STATUS = config["status"]
IMAGE = config["image"]
COLOUR = config["embedcolour"]

bot = commands.Bot(command_prefix=PREFIX, self_bot = True, case_insensitive=True)
bot.remove_command("help")

@bot.event
async def on_ready():
  print('Online!!!')
  await bot.change_presence(activity=discord.Game(name=f'{STATUS}'))

@bot.command(aliases=["em"])
async def embed(ctx, name=None, *, des=None):
    await ctx.message.delete()
    embed = discord.Embed(title=f'{name}', description=f"{des}", color=f"{COLOUR}")
    await ctx.send(embed=embed)

@bot.command(aliases=["off"])
async def shutdown(ctx):
    await ctx.bot.logout()

@bot.command(aliases=["commands", "help"])
async def cmds(ctx):
    embed = discord.Embed(title="**Self Bot**", description="This self-bot was created by Ex-God", color=f"{COLOUR}")
    embed.add_field(name="Whois", value="To get the user info of mentioned user", inline=False)
    embed.add_field(name="Help", value="Shows this command", inline=False)
    embed.add_field(name="Avatar", value="Get avatar of the mentioned user", inline=False)
    embed.add_field(name="Purge", value="delete messages", inline=False)
    embed.add_field(name="Shutdown", value="to shudown/logout the selfbot", inline=False)
    embed.set_image(url=f"{IMAGE}")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/907139810081275916/908232589419094086/pepe-hack-hack.gif")
    await ctx.send(embed=embed)

@bot.command(aliases=["av"])
async def avatar(ctx, member: discord.Member = None):
    if not member:  
        member = ctx.message.author  
    roles = [role for role in member.roles]
    embed = discord.Embed(color=f"{COLOUR}", timestamp=ctx.message.created_at,
                          title=f"Avatar of - {member}")
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


@bot.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  
        member = ctx.message.author  
    roles = [role for role in member.roles]
    embed = discord.Embed(color=f"{COLOUR}" , timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@bot.command
async def kick(ctx,member : discord.Member,*,reason= "No reason was provided"):
    await member.kick(reason=reason)
    embed = discord.Embed(title="Kicked", description=f"{member.mention} was Kicked", color=f"{COLOUR}")
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)

@bot.command
async def ban(ctx,member : discord.Member,*,reason= "No reason was provided"):
    await member.ban(reason=reason)
    embed = discord.Embed(title="Banned", description=f"{member.mention} was Banned", color=f"{COLOUR}")
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=["clean"])
async def purge(ctx,amount=2):
    await ctx.channel.purge(limit = amount)
    await ctx.send("cleared ✅", delete_after=3)

bot.run(TOKEN, bot=False)