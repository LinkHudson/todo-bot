# This example requires the 'message_content' intent.
from pprint import pprint

import discord
from discord.ext import commands
from lxml.html._diffcommand import description
from botcommands.school_closings import get_school_closings
from os import environ

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True            # server join/ready events, required for slash commands
intents.messages = True          # message events (e.g., for message-related events like on_message_delete)
intents.reactions = True         # reactions


# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', description=description, intents=intents, application_id=environ.get('APPLICATION_ID'))

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    print("test")
    await ctx.send(left + right)

@bot.command()
async def closings(ctx, school: str = None):
    if school:
        schools = [school.lower()]
    else:
        schools = ['uniontown', 'albert']

    closings, no_school = get_school_closings(schools, observations=True)

    await ctx.send(closings['msg'])

@bot.tree.command(name="hi")
async def hi(interaction: discord.Interaction):
    await interaction.response.send_message("Hi, slash!")

@bot.event
async def on_ready():
    try:
        # for instant visibility during development:
        await bot.tree.sync(guild=discord.Object(id=environ.get('GUILD_ID')))
        print("Commands synced to guild")
    except Exception as e:
        print("Sync failed:", e)
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    if content.startswith('hello'):
        await message.channel.send('World!')


    await bot.process_commands(message)


bot.run(environ.get('TOKEN'))

