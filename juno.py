import discord
from discord.ext import commands
import json
with open('config.json', 'r') as f:
    config = json.load(f)
token = config['token']

client = discord.Client(intents=discord.Intents.default())
#client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="around"))

client.run(token)