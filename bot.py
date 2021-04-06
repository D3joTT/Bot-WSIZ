import json

import discord as discord
from discord.ext import commands
from discord.utils import get, find

bot = commands.Bot(command_prefix=['!', '/'])
bot.remove_command('help')


with open("config/config.json", "r+") as jsonFile:
    data = json.load(jsonFile)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=data["status"]))
    print("Bot enabled")


@bot.command(name="panel")
async def create_panel(ctx):
    await ctx.message.delete()
    ret_str = data["available"]

    # "⠀\n💻 - Programista\n🎨 - Grafik\n🌐 - Web Dev\n🔒 - Administrator Sieci"

    embed = discord.Embed(title=data["chooseRole"], color=0x1ae0a8)
    embed.set_thumbnail(url=data["url"])
    embed.add_field(name=data["getRole"], value=ret_str)
    message = await ctx.send(embed=embed)
    data["panel"] = message.id
    jsonFile.seek(0)
    json.dump(data, jsonFile)
    jsonFile.truncate()
    emojis = data["emojis"]

    for emoji in emojis:
        await message.add_reaction(emoji)


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if payload.member.id == 761258280675704863:
        return
    if message_id == data["panel"]:
        guild_id = payload.guild_id
        guild = find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == '💻':
            role = get(guild.roles, id=761478551907074048)
        elif payload.emoji.name == '🎨':
            role = get(guild.roles, id=761478598749454356)
        elif payload.emoji.name == '🌐':
            role = get(guild.roles, id=761478681772032033)
        elif payload.emoji.name == '🔒':
            role = get(guild.roles, id=761478629292245022)
        else:
            return

        if role is not None:
            await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == data["panel"]:
        guild_id = payload.guild_id
        guild = find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == '💻':
            role = get(guild.roles, id=761478551907074048)
        elif payload.emoji.name == '🎨':
            role = get(guild.roles, id=761478598749454356)
        elif payload.emoji.name == '🌐':
            role = get(guild.roles, id=761478681772032033)
        elif payload.emoji.name == '🔒':
            role = get(guild.roles, id=761478629292245022)
        else:
            return

        if role is not None:
            member = find(lambda m: m.id == payload.user_id, guild.members)
            await member.remove_roles(role)


@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, id=761479584780648448)
    await member.add_roles(role)
    ret_str = "Cras in efficitur sem, eget sodales dolor."
    embed = discord.Embed(title=data["welcome"], color=0x1ae0a8)
    embed.set_thumbnail(url=data["url"])
    embed.set_footer(text="⠀⠀₪⠀⠀" + member.display_name)
    embed.add_field(name="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", value=ret_str)
    await bot.get_channel(761482022690226207).send(embed=embed)


bot.run(data["token"])
