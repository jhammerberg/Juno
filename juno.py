from llama_cpp import Llama
import json

with open("config.json", "r") as f:
    config = json.load(f)
system_prompt = config["system-prompt"]
model = config["model"]

previous_msgs = [{"role": "system", "content": system_prompt}]

llm = Llama(
  model_path=model,
  n_ctx=32768,            # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=0,         # The number of layers to offload to GPU, if you have GPU acceleration available
  verbose=False
)

def chat(prompt):
  global previous_msgs
  previous_msgs.append({"role": "user", "content": prompt})
  output = llm(
               str(previous_msgs),  # The prompt to use for the completion
               max_tokens=512,
               stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
               echo=False
              )
  text = output["choices"][0]["text"]
  try:
    return json.loads(text)["text"]
  except:
    return text

while True:
  prompt = input("Prompt: ")
  print(chat(prompt))