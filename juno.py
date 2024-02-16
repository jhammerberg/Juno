from llama_cpp import Llama
import time
import json

with open("config.json", "r") as f:
    config = json.load(f)
system_prompt = config["system-prompt"]
model = config["model"]

previous_msgs = [{"role": "system", "content": system_prompt}]

llm = Llama(
  model_path=model,
  n_ctx=32768,            # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=12,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=50,         # The number of layers to offload to GPU, if you have GPU acceleration available
  verbose=False
)

def chat(prompt):
  global previous_msgs
  previous_msgs.append({"role": "user", "content": prompt})

  stream = llm.create_chat_completion(
    model=model,
    messages = previous_msgs,
    response_format = {"type": "json_object",},
    max_tokens=512,
    stream=True
  )
  return stream

while True:
  prompt = input("\033[32mPrompt:\033[0m ")
  stream = chat(prompt)
  output = ""
  final_output = ""
  print("\033[1A", end="\033[34m", flush=True)
  for chunk in stream:
    # The first and last chunks will not have useful output text, so we filter them with this if statement
    if ('content') in (str(chunk['choices'][0]['delta'])):
      final_output += chunk['choices'][0]['delta']['content']
      output = chunk['choices'][0]['delta']['content']
      # Print the output, one character at a time, adding to the same line.
      for char in output:
        print(char, end='', flush=True)
        time.sleep(0.008)
  previous_msgs.append({"role": "assistant", "content": final_output})
  print("\033[0m")