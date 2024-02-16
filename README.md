update, we're using this model:
https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF

# Introduction
Juno is a large language model designed to be an open-source, multi-purpose general artificial intellegence platform.

Juno is an advanced API for the Dolphin-2.5-mixtral-8x7b-GGUF model with interfaces to allow for Discord integration, function calls, and long term memory through embeddings and vector databases (eventually)

This is version 2 of Juno, the first version which you can find [here](https://github.com/jhammerberg/Juno) is primarily just a discord bot with OpenAI API integration. While that API is awesome and very easy to develop with, it also costs money and has some major limitations.

The goal for Juno Mk II is to be entirely free to run and use, while maintaining or even extending the capabilites of Juno Mk I. 

As mentioned before, this new version of Juno is just an API at it's core, to add functionality and to simplify the Dolphin-2.5 open-source language model. The reason for this is not only to provide code modularity, but also to give the option to extend Juno past the limitations of a Discord bot through a web-interface later down the line. If you are a developer and want to use this as a reference, it also helps with that!

# Dolphin-2.5
As mentioned before, this AI uses the Dolphin-2.5 model by "TheBloke" on Hugging Face as it's core. You may be able to change out this model for a different or newer one, but it may require modifications. Check out the great documentation [here](https://huggingface.co/TheBloke/dolphin-2.5-mixtral-8x7b-GGUF)!

The main motivation for choosing this model in particular over something like Llama-v2 is because of the uncensored nature of Dolphin-2.5 which is helpful, not only for getting over the annoying safeguards OpenAI and Meta introduce into their models, but it also increases the quality of the output, making this model somewhere between Llama and GPT-4. Oh, and of course it's free and open-source!

# Installation and usage
This project is still very much in the early stages of development, but for basic environment set up you will need to:
1. Clone this (branch of the) reposity of course\
```git clone --branch Mark-II https://github.com/jhammerberg/Juno```
2. Install Python ***3.11.8 64-bit*** and make an environment with it
    - You can have a newer or older version of Python still be your primary installation version if you want, because we will be making a seperate environment that will use specifically 3.11.8 64-Bit by specifying the version when we create it.
    - If you already have this version, check that it's the ***64-bit*** version because otherwise PyTorch won't be able to be installed, or even found.
3. Make an environment for installation tools\
    ```/path/to/python3.11.8-64bit -m venv .juno-env```
    - Run the activation file
        - Windows (PowerShell, as Admin):\
        Allow for file execution:\
        ```set-executionpolicy remotesigned```\
        Run the script:\
        ```.\.juno-env/Scripts/Activate.ps1```
        - Linux:\
        ```source .juno-env/bin/activate```
4. Clone the Dolphin-2.5-Mixtral-8x7b-GGUF model from Huggingface 
    - Install Hugging Face modules\
    ```pip install --upgrade huggingface_hub```\
    ```pip install -U "huggingface_hub[cli]"```
    - Download the model
    ```bash
    huggingface-cli download TheBloke/dolphin-2.5-mixtral-8x7b-GGUF dolphin-2.5-mixtral-8x7b.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
    ```
    (This is like 25Gb so it'll take a while)
5. Install required Dolphin-2.5 specific libraries
(from the [Dolphin-2.5 install instructions](https://huggingface.co/TheBloke/dolphin-2.5-mixtral-8x7b-GGUF#first-install-the-package))
```py
# Base ctransformers with no GPU acceleration
pip install llama-cpp-python
# With NVidia CUDA acceleration
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
# Or with OpenBLAS acceleration
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
# Or with CLBLast acceleration
CMAKE_ARGS="-DLLAMA_CLBLAST=on" pip install llama-cpp-python
# Or with AMD ROCm GPU acceleration (Linux only)
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" pip install llama-cpp-python
# Or with Metal GPU acceleration for macOS systems only
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# In windows, to set the variables CMAKE_ARGS in PowerShell, follow this format; eg for NVidia CUDA:
$env:CMAKE_ARGS = "-DLLAMA_OPENBLAS=on"
pip install llama-cpp-python
```
(I've only ever used the normal installation, without GPU acceleration, so tell me if others cause issues)
6. Make and edit a `.env` file with your Discord Bot's credentials\
*This is DIFFERENT than the Python virtual environment we made earlier, this is a seperate file to store sensitive information like keys*\
It should be formatted like this:\
`DISCORD_KEY="BOT TOKEN"`\
7. Run the start script for your OS\
`start.sh` or `start.bat`
