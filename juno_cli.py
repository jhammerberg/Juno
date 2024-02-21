import juno
import time

global previous_msgs
previous_msgs = []

Juno = juno.Juno( # naming is a bit confusing but, we're making the "Juno" object here, from the "juno" module and the class "Juno" 
  config_file="config.json", 
  verbose=False,
  llama_verbose=False
) # Create a Juno object with the config file

"""
One of many different ways to interact with the chat stream. This one is a simple command line interface.
"""
def CLI_Chat(prompt_input):
    global previous_msgs
    stream = Juno.chat_stream(previous_msgs, prompt_input)                # Get a stream given the prompt
    final_output = ""                                                     # We need a variable to hold the message
    print("\033[1A", end="\033[34m", flush=True)                          # Set color to blue
    for chunk in stream:                                                  # Iterate through the stream                                                
      chunk = chunk['choices'][0]['delta']                                # Grabs just the delta from the response
      if ('content') in (str(chunk)):                                     # The first and last chunks will not have useful output text, so we filter them with this if statement
          final_output += chunk['content']                                # Because we need the finished output to be a string for later chat history, we need a seperate variable to hold the entire message.
          for char in chunk['content']:                                   # Print the output, one character at a time, adding to the same line. This is mostly cosmetic.
              print(char, end='', flush=True)                             # Prints characters, "end=''" prevents the automatic newline character from being added
              time.sleep(0.008)                                           # Can be adjusted to change the speed of the output, this can bottleneck the actual text generation speed if it's too slow
    previous_msgs.append({"role": "assistant", "content": final_output})  # Add the entire message to the chat history for context.
    print("\033[0m")                                                      # Resets the color to the default

def main():
  while True:
    prompt_input = input("\033[32mPrompt:\033[0m ")
    CLI_Chat(prompt_input)

if __name__ == "__main__":
  main()