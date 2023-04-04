import discord
import openai
from discord.ext import commands
import json
with open('config.json', 'r') as f:
    config = json.load(f)
token = config['token']
apiKey = config['api-key']

openai.api_key = apiKey
client = discord.Client(intents=discord.Intents.all())
#client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="around"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'juno' in message.content.lower():
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content" : "You are the helpful AI assistant 'Juno'. Your role is to give answers in the style that Jarvis from Iron Man would. Give short answers, only as long as a few sentences."},
                {"role": "user", "content": message.content}
            ]
        )
        await message.channel.send(completion['choices'][0]['message']['content'])

client.run(token)