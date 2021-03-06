import datetime
# import io
import json
import logging
import os
import random
from itertools import cycle

import discord
from discord.ext import commands, tasks
# from dotenv import load_dotenv
from quart import Quart

original_dir = os.getcwd()
jsons = ['applications.json', 'counts.json', 'economy.json', 'guilds_data.json', 'prefix.json', 'reaction_roles.json', 'reports.json', 'suggestions.json', 'tickets.json',
         'tunnels.json', 'users.json', 'voice_text.json']

try:
    os.listdir('data')
except FileNotFoundError:
    os.mkdir('data')
finally:
    for file in jsons:
        if file not in os.listdir('data'):
            open(file, "w").write('{\n\n}')
os.chdir(original_dir)
# env = io.StringIO(initial_value=open('Bot/.env', encoding='utf-8').read())
# load_dotenv(stream=env)
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DEFAULT_PREFIX')
TICKET_EMOJI = os.getenv('DEFAULT_TICKET_EMOJI')
DELIMITER = os.getenv('DEFAULT_DELIMITER_FOR_ENV')
PORT_NUMBER = os.getenv('PORT_NUMBER')
HOST_NUMBER = os.getenv('HOST_NUMBER')
USERS_FILE = os.getenv('USERS_JSON')
PREFIX_FILE = os.getenv('PREFIX_JSON')
GUILD_FILE = os.getenv('GUILDS_JSON')
VOICE_TEXT_FILE = os.getenv('VOICE_TEXT_JSON')
COUNTS_FILE = os.getenv('COUNTS_JSON')
SUGGESTIONS_FILE = os.getenv('SUGGESTIONS_JSON')
REPORTS_FILE = os.getenv('REPORTS_JSON')
TICKETS_FILE = os.getenv('TICKETS_JSON')
REACTION_ROLES_FILE = os.getenv('REACTION_ROLES_JSON')
APPLICATIONS_FILE = os.getenv('APPLICATIONS_JSON')
TUNNELS_FILE = os.getenv('TUNNELS_JSON')
ECONOMY_FILE = os.getenv('ECONOMY_JSON')
CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')


def get_prefix(bot_1, message):
    try:
        prefix_list = json.load(open(bot_1.prefix_json, "r"))
    except (json.JSONDecodeError, FileNotFoundError):
        prefix_list = {}
    try:
        if str(message.guild.id) not in prefix_list.keys():
            prefix_list[str(message.guild.id)] = {"prefix": list(PREFIX.split(DELIMITER))}
    except AttributeError:
        pass
    with open(bot_1.prefix_json, "w") as f:
        json.dump(prefix_list, fp=f, indent='\t')
    try:
        return commands.when_mentioned_or(*prefix_list[str(message.guild.id)]["prefix"])(bot, message)
    except AttributeError:
        return commands.when_mentioned_or(*list(PREFIX.split(DELIMITER)))(bot, message)


init_cogs = [f'Bot.cogs.{filename[:-3]}' for filename in os.listdir('Bot/cogs') if filename.endswith('.py')]
app = Quart(__name__)
bot = commands.Bot(command_prefix=get_prefix)


@app.route("/")
def hello():
    return "Hello from {}".format(bot.user.name)


oauth_url = discord.utils.oauth_url(client_id=CLIENT_ID, permissions=discord.Permissions(8))

bot.start_time = datetime.datetime.utcnow()
bot.prefix_default = PREFIX.split(DELIMITER)
bot.ticket_emoji_default = TICKET_EMOJI.split(DELIMITER)
bot.users_json = USERS_FILE
bot.prefix_json = PREFIX_FILE
bot.guilds_json = GUILD_FILE
bot.voice_text_json = VOICE_TEXT_FILE
bot.counts_json = COUNTS_FILE
bot.suggestions_json = SUGGESTIONS_FILE
bot.reports_json = REPORTS_FILE
bot.tickets_json = TICKETS_FILE
bot.applications_json = APPLICATIONS_FILE
bot.reaction_roles_json = REACTION_ROLES_FILE
bot.tunnels_json = TUNNELS_FILE
bot.economy_json = ECONOMY_FILE
bot.invite_url = oauth_url
bot.start_number = 1000000000000000
bot.init_cogs = init_cogs

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command Not found!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have enough permissions.")
    elif isinstance(error, commands.CheckAnyFailure):
        await ctx.send("".join(error.args))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("".join(error.args))
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You're only allowed to use this command in Direct or Private Message only!")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("You're not a owner till now!")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("You can't send this commands here!")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send("The command you send is on cooldown!")
    else:
        raise error


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name=f"OpenCity • Type {random.choice(bot.prefix_default)}help to get started"))
    # guild = discord.utils.get(client.guildTry .helps, id=GUILD_ID)
    # roles_needed = ["Muted Members", "Banned Members", "Kicked Members"]
    for guild_index, guild in enumerate(bot.guilds):
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members of {guild.name} are:\n - {members}')
        if guild_index != (len(bot.guilds) - 1):
            print('\n\n\n', end="")

        # role_names = [role.name for role in guild.roles]

# for role in roles_needed:
# 	if role not in role_names:
# 		await guild.create_role(name=role)


for filename in os.listdir('Bot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Bot.cogs.{filename[:-3]}')


@tasks.loop(hours=1)
async def my_presence_per_day():
    await bot.wait_until_ready()
    statuses = cycle([discord.Status.do_not_disturb, discord.Status.online, discord.Status.offline, discord.Status.idle, discord.Status.dnd])
    activities = cycle([discord.Game(name=f"OpenCity • Type {random.choice(bot.prefix_default)}help to get started"),
                        discord.Streaming(name=f"OpenCity • Type {random.choice(bot.prefix_default)}help to get started", url="https://www.twitch.tv/opencitybotdiscord"),
                        discord.Activity(type=discord.ActivityType.listening, name=f"OpenCity • Type {random.choice(bot.prefix_default)}help to get started"),
                        discord.Activity(type=discord.ActivityType.watching, name=f"OpenCity • Type {random.choice(bot.prefix_default)}help to get started")])
    status = next(statuses)
    activity = next(activities)
    await bot.change_presence(status=status, activity=activity)


@tasks.loop(seconds=15)
async def add_guild_to_json():
    await bot.wait_until_ready()
    guilds_data = json.load(open(bot.guilds_json))
    for guild in bot.guilds:
        if str(guild.id) not in guilds_data.keys():
            guilds_data[str(guild.id)] = {}
            guilds_data[str(guild.id)]['enabled'] = bot.init_cogs
            guilds_data[str(guild.id)]['disabled'] = [""]
    with open(bot.guilds_json, "w+") as f:
        json.dump(guilds_data, f, indent='\t')


@bot.command()
@commands.is_owner()
async def reload_all_extensions(ctx):
    for filename1 in os.listdir('Bot/cogs'):
        if filename1.endswith('.py'):
            bot.unload_extension(f'Bot.cogs.{filename1[:-3]}')
            bot.load_extension(f'Bot.cogs.{filename1[:-3]}')
    await ctx.send("Reloaded all extensions!")


my_presence_per_day.start()
add_guild_to_json.start()

# @bot.command()
# async def guild_create(ctx):
# 	guild: discord.Guild = bot.get_guild(711869134874607688)
# 	channel: discord.TextChannel = await guild.create_text_channel(name="Somehow-ok")
# 	invite = await channel.create_invite()
# 	await ctx.send(invite.url)


bot.loop.create_task(app.run_task(host=HOST_NUMBER, port=int(PORT_NUMBER), debug=True))
bot.run(TOKEN)
