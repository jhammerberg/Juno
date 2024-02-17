from llama_cpp import Llama
import json

class Juno:
  def __init__(self, config_file="config.json", n_ctx=32768, n_threads=12, n_gpu_layers=200, llama_verbose=False, verbose=True):
    self.n_ctx = n_ctx
    self.n_threads = n_threads
    self.n_gpu_layers = n_gpu_layers
    self.llama_verbose = llama_verbose
    self.verbose = verbose

    with open(config_file, "r") as f:
      config = json.load(f)
    
    self.model = config["model"]
    self.chat_tokens = config["max-tokens"]
    self.system_prompt = ({"role": "system", "content": config["system-prompt"]})

    if not self.verbose:
      print("\033[2J")
      print("Initializing...", end="\r")

    self.llm = Llama(
      model_path=self.model,
      n_ctx=self.n_ctx,
      n_threads=self.n_threads,
      n_gpu_layers=self.n_gpu_layers,
      verbose=self.llama_verbose
    )

    if not self.verbose:
      print("Initialization complete.")

  def chat_stream(self, prompt, previous_msgs):
    if previous_msgs == []:
      previous_msgs = [self.system_prompt]
    previous_msgs.append({"role": "user", "content": prompt})

    stream = self.llm.create_chat_completion(
      model=self.model,
      messages=previous_msgs,
      response_format={"type": "json_object"},
      max_tokens=self.chat_tokens,
      stream=True
    )

    return stream

  def chat_completion(self, prompt, previous_msgs):
    if previous_msgs == []:
      previous_msgs = [self.system_prompt]
    previous_msgs.append({"role": "user", "content": prompt})

    completion = self.llm.create_chat_completion(
      model=self.model,
      messages=previous_msgs,
      response_format={"type": "json_object"},
      max_tokens=self.chat_tokens
    )

    return completion