# Introduction
Juno is a large language model designed to be an open-source, multi-purpose general artificial intelligence platform.

Juno is an advanced API for the Dolphin-2.6-mistral-7b.Q5_K_M.gguf model with interfaces to allow for Discord integration, function calls, and long-term memory through embeddings and vector databases (eventually).

*Note: You can use other GGUF models with is project pretty easily, just change the 'model' key in the config.json*\
*HOWEVER: Other models like [dolphin-2_6-phi-2](https://huggingface.co/cognitivecomputations/dolphin-2_6-phi-2*) which I think could work REALLY well for this project, use a different format and are untested.*

This is version 2 of Juno, the first version which you can find [here](https://github.com/jhammerberg/Juno) is primarily just a discord bot with OpenAI API integration. While that API is awesome and very easy to develop with, it also costs money and has some major limitations.

The goal for Juno Mk II is to be entirely free to run and use, while maintaining or even extending the capabilities of Juno Mk I.

As mentioned before, this new version of Juno is just an API at its core, to add functionality and to simplify the Dolphin-2.6 open-source language model. The reason for this is not only to provide code modularity but also to give the option to extend Juno past the limitations of a Discord bot through a web interface later down the line. If you are a developer and want to use this as a reference, it also helps with that!

# Dolphin-2.6
As mentioned before, this AI uses the Dolphin-2.6-mistral-7b.Q5_K_M.gguf model by "TheBloke" on Hugging Face as its core. You may be able to change out this model for a different or newer one, but it may require modifications. Check out the great documentation [here](https://huggingface.co/TheBloke/dolphin-2.6-mistral-7b.Q5_K_M.gguf)!

The main motivation for choosing this model in particular over something like Llama-v2 is because of the uncensored nature of Dolphin-2.6, which is helpful, not only for getting over the annoying safeguards OpenAI and Meta introduce into their models, but it also increases the quality of the output, making this model somewhere between Llama and GPT-4. Oh, and of course, it's free and open-source!

# Installation and usage
This project is still very much in the early stages of development, but for basic environment setup, you will need to:
1. Clone this (branch of the) repository, of course\
`git clone --branch Mark-II https://github.com/jhammerberg/Juno`
2. Install Python ***3.11.8 64-bit*** and make an environment with it
    - You can have a newer or older version of Python still be your primary installation version if you want, because we will be making a seperate environment that will use specifically 3.11.8 64-Bit by specifying the version when we create it.
    - If you already have this version, check that it's the ***64-bit*** version because otherwise PyTorch won't be able to be installed, or even found.
3. Make an environment for installation tools\
    ```/path/to/python3.11.8-64bit -m venv .juno-env```
    - Run the activation file
        - Windows (PowerShell, as Admin):\
        Allow for file execution:\
        `set-executionpolicy remotesigned`\
        Run the script:\
        `.\.juno-env/Scripts/Activate.ps1`
        - Linux:\
        `source .juno-env/bin/activate`
4. Clone the Dolphin-2.5-Mixtral-8x7b-GGUF model from Huggingface 
    - Install Hugging Face modules\
    `pip install --upgrade huggingface_hub`\
    `pip install -U "huggingface_hub[cli]"`
    - Download the model
    ```bash
    huggingface-cli download TheBloke/dolphin-2.6-mistral-7B-GGUF dolphin-2.6-mistral-7b.Q5_K_M.gguf --local-dir . --local-dir-use-symlinks False
    ```
    (This is like 5.13Gb so it'll take a while)
5. Install required llama-cpp-python library
(from the [Dolphin-2.6 install instructions](https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF#first-install-the-package))
- Download the CUDA Toolkit from [here](https://developer.nvidia.com/cuda-toolkit-archive) and install it\
*This is optional, but inferencing (the time it takes to generate text) becomes much longer*\
*You will also leave out the CMAKE_ARGS line while installing llama-cpp-python*

Windows:
```py
$env:CMAKE_ARGS = "-DLLAMA_CUBLAS=on"
$env:FORCE_CMAKE = 1
pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```
---
Linux:
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on"
FORCE_CMAKE = 1
pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```
**At least on Windows, you will have to restart your computer in order for the environment variables to change and the next command to run properlly**
- To see if your CUDA installation is working, run the following command:
```bash
python -c "import llama_cpp as llama; print(llama.cuda_version())"
```
6. (OPTIONAL) Make and edit a `.env` file with your Discord Bot's credentials\
*This is DIFFERENT than the Python virtual environment we made earlier, this is a seperate file to store sensitive information like keys*\
It should be formatted like this:\
`DISCORD_KEY="BOT TOKEN"`
---
## Usage
To run a basic version of Juno in the terminal run the following command:
```bash
python juno-cli.py
```
*This example is for Windows and has some special ANSI control characters to make the output look nice, so it may not work on Linux or MacOS. If you want to use it on those systems, you can remove the ANSI control characters from the `print` statements in `juno-cli.py`*

---
To run Juno as a **Discord Bot**, you will need to have a `.env` file with your Discord Bot's credentials, and then run the following command:
```bash
python juno-discord.py
```
*This has some libraries that you probably don't have, so install them if you have some errors*