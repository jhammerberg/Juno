import asyncio
import time
from bs4 import BeautifulSoup
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime
import discord
import openai
import pytz
import json
import re
import os

global system_prompt, previous_msgs
with open("config.json", "r") as f:
    config = json.load(f)
system_prompt = config["system-prompt"]
functions = config["functions"]

if not os.path.isfile(".env"): # Check if there's a .env file and throw an error if there isn't
    print("\033[91mERROR: No .env file found. Please create one with the keys 'DISCORD_KEY' and 'OPENAI_KEY'.\033[0m")
    exit()
load_dotenv()
discord_key = os.environ.get("DISCORD_KEY")
openai_key = os.environ.get("OPENAI_KEY")

openai.api_key = openai_key
client = discord.Client(intents=discord.Intents.all())
commands = app_commands.CommandTree(client)
previous_msgs = [{"role": "system", "content": system_prompt}]

def create_image(prompt):
    #create an image from the prompt
    image_url = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    image = {
        "image_url": image_url['data'][0]['url']
    }
    
    return json.dumps(image)

def sanitize_username(username): #openai needs the username to fit a certain format 
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "", username)
    return sanitized[:64]

def get_time(timezone):
    #get current time in said timezone
    time = {
        "timezone": timezone,
        "time": datetime.now(pytz.timezone(timezone)).strftime("%m/%d/%Y %H:%M:%S")
    }
    #return in json format
    return json.dumps(time)

def complete_chat(message, client):
    global previous_msgs
    previous_msgs.append({"role": "user", "name": sanitize_username(client), "content": message})
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=previous_msgs,
        functions=functions,
        function_call="auto",
        stream=True
    )
    
    response = next(completion).choices[0].delta #get the response from the json
    #print(json.dumps(next(completion)))
    if response.get("function_call"): #I copied this from the openai docs, I don't know how it works
        available_functions = {
            "get_time": get_time,
            "create_image": create_image
        }
        function_name = response["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_parameters = json.loads(response["function_call"]["arguments"])
        function_response = function_to_call(**function_parameters)

        previous_msgs.append(response)
        previous_msgs.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response
            }
        )
        second_completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=previous_msgs,
            stream=True
        )
        return second_completion
    return completion
    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="GPT-4"))
    await commands.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'juno' in message.content.lower():
        async with message.channel.typing(): #gives a typing indicator while the response is being generated
            completion_object = complete_chat(message.content, str(message.author))
            message_string = ""
            bots_message = await message.channel.send("...") #Send a message to edit later
            i = 0
            for chunk in completion_object:
                i=i+1 #using 'i' cause you can't use chunk since it's an "openaiobject" not an index
                if "content" in chunk.choices[0].delta:
                    message_string = message_string + chunk.choices[0].delta["content"]
                else:
                    return
                if message_string != "" and i%10==0: #only send every seventh message and check if the first chunk is empty
                    await bots_message.edit(content=message_string)

@commands.command(name= "clear_chat", description= "Clears the chat history given to ChatGPT.")
async def clear_chat(interaction):
    global previous_msgs; system_prompt
    previous_msgs = [{"role": "system", "content": system_prompt}] 
    await interaction.response.send_message("Chat History Cleared")

@commands.command(name= "give_role", description= "Gives a specific role to whoever uses it.")
async def give_role(interaction: discord.Interaction, name: str):
    server = client.get_guild(interaction.channel.guild.id)
    role = discord.utils.get(server.roles, name=name)
    await interaction.user.add_roles(role)
    await interaction.response.send_message("Role Added")

if __name__ == "__main__":
    os.system("git pull")
    client.run(discord_key)