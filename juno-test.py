from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime
from llama_cpp import Llama
import requests
import asyncio
import discord
import pytz
import re
import json
import os

global system_prompt, previous_msgs
with open("config.json", "r") as f:
    config = json.load(f)
system_prompt = config["system-prompt"]
model = config["model"]

if not os.path.isfile(".env"): # Check if there's a .env file and throw an error if there isn't
    print("\033[91mERROR: No .env file found. Please create one with the keys 'DISCORD_KEY'\033[0m")
    exit()
load_dotenv()
discord_key = os.environ.get("DISCORD_KEY")

llm = Llama(
  model_path=model,
  n_ctx=32768,            # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=12,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=0,         # The number of layers to offload to GPU, if you have GPU acceleration available
  chat_format="llama-2",
  verbose=False
) #create the llama object

client = discord.Client(intents=discord.Intents.all())
commands = app_commands.CommandTree(client)
previous_msgs = [{"role": "system", "content": system_prompt}]

def sanitize_username(username): #openai needs the username to fit a certain format 
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "", username)
    return sanitized[:64]

def get_functions():
    #procedurally generate the functions for the openai api
    functions = []
    for function_name in config["functions"]:
        function_info = config["functions"][function_name]
        functions.append({
            "name": function_name,
            "description": function_info["description"],
            "parameters": {
                "type": "object",
                "properties": {
                    function_info["property_name"]: {
                        "type": "string",
                        "description": function_info["property_description"]
                    }
                }
            }
        })
    return functions

def complete_chat(message, client):
    global previous_msgs
    previous_msgs.append({"role": "user", "name": sanitize_username(client), "content": message})
    completion = llm.create_chat_completion(
        model=model,
        messages=previous_msgs,
        functions=get_functions(),
        function_call="auto"
    )
    response = completion['choices'][0]['message'] #get the response from the json
    if response.get("function_call"): #I copied this from the openai docs, I don't know how it works
        available_functions = {
            "get_time": get_time,
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
        second_completion = llm.create_chat_completion(
            model=model,
            messages=previous_msgs,
        )
        return second_completion['choices'][0]['message']['content']
    return response['content'] #return the message inside the json

def get_time(timezone):
    #get current time in said timezone
    time = {
        "timezone": timezone,
        "time": datetime.now(pytz.timezone(timezone)).strftime("%m/%d/%Y %H:%M:%S")
    }
    #return in json format
    return json.dumps(time)

@client.event
async def on_ready():
    print("We have logged in as " + str(client.user))
    await client.change_presence(activity=discord.Game(name="Dolphin-2.5 🐬"))
    #await commands.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'juno' in message.content.lower():
        async with message.channel.typing(): #gives a typing indicator while the response is being generated
            await message.channel.send(complete_chat(message.content, str(message.author)))

@commands.command(name= "clear_chat", description= "Clears the chat history given to ChatGPT.")
async def clear_chat(interaction):
    global previous_msgs; system_prompt
    previous_msgs = [{"role": "system", "content": system_prompt}] 
    await interaction.response.send_message("Chat History Cleared")

if __name__ == "__main__":
    client.run(discord_key)