from discord import app_commands
from dotenv import load_dotenv
import asyncio
import discord
import juno
import json
import os
import re

global previous_msgs
previous_msgs = []

if not os.path.isfile(".env"): # Check if there's a .env file and throw an error if there isn't
    print("\033[91mERROR: No .env file found. Please create one with the keys 'DISCORD_KEY'\033[0m")
    exit()
load_dotenv()
discord_key = os.environ.get("DISCORD_KEY")
client = discord.Client(
    intents=discord.Intents.all()
)
commands = app_commands.CommandTree(client)

Juno = juno.Juno( # naming is a bit confusing but, we're making the "Juno" object here, from the "juno" module and the class "Juno" 
  config_file="config.json", 
  verbose=False,
  llama_verbose=False
) # Create a Juno object with the config file

def sanitize_username(username): #openai needs the username to fit a certain format 
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "", username)
    return sanitized[:64]

@client.event
async def on_ready():
    print("We have logged in as " + str(client.user))
    await client.change_presence(activity=discord.Game(name="Dolphin-2.5 🐬"))
    await commands.sync()

@client.event
async def on_message(message):
    global previous_msgs

    if message.author == client.user:                                               # If the message is from the bot, don't do anything
        return                                                                      
    if 'juno' in message.content.lower():                                           # If the message contains "juno" in any case
        async with message.channel.typing():                                        # Gives a typing indicator while the response is being generated
            author = sanitize_username(str(message.author))                         
            prompt = str(message.content)
            stream = Juno.chat_stream(previous_msgs, prompt, author)                # Get a stream given the prompt
            message_string = ""                                                     # We need a variable to hold the message
            bots_message = await message.channel.send("...")                        # Send a message to edit later
            i = 0                                                                   # Counter so that we change how often we send a message
            for chunk in stream:                                                    # Iterate through the stream  
                i=i+1                                                               # We have to use a seperate counter because you can't use the index of a for loop with an async generator
                chunk = chunk['choices'][0]['delta']                                # Grabs just the delta from the response
                if ('content') in (str(chunk)):                                     # The first and last chunks will not have useful output text, so we filter them with this if statement
                    message_string += chunk['content']                              # Add the content to the message string
                if (message_string != "") and (i >= 2) and (i % 5 == 0):            # If the message string is not empty, skip the first couple of chunks because they're newlines and only send every few chunks to avoid rate limits
                    await bots_message.edit(content=message_string)                 # Edit the message with the new content
            previous_msgs.append({"role": "assistant", "content": message_string})  # Add the entire message to the chat history for context.
            await bots_message.edit(content=message_string)                         # Edit the message to have the final content

@commands.command(name= "clear_chat", description= "Clears the chat history given to Juno.")
async def clear_chat(interaction):
    global previous_msgs
    previous_msgs = [] 
    await interaction.response.send_message("Chat History Cleared")

if __name__ == "__main__":
    client.run(discord_key)