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
      self.config = json.load(f)
    
    if self.config["functions-enable"]: # doing it this way allows us to ignore the function file (and modules) if it's not enabled
      import juno_functions
      Juno_functions = juno_functions.Juno_functions()
      self.available_functions = juno_functions.Juno_functions.available_functions
      self.function_call = "auto"
    else:
      self.function_call = "none"
    self.model = self.config["model"]
    self.chat_tokens = self.config["max-tokens"]
    self.system_prompt = ({"role": "system", "content": self.config["system-prompt"]})
    
    if self.verbose:
      print("\033[2J")
      print("Initializing...", end="\r")

    self.llm = Llama(
      model_path=self.model,
      n_ctx=self.n_ctx,
      n_threads=self.n_threads,
      n_gpu_layers=self.n_gpu_layers,
      verbose=self.llama_verbose,
    )

    if self.verbose:
      print("Initialization complete.")

  def get_functions(self):
    #procedurally generate the functions from the config file
    functions = []
    for function_name in self.config["functions"]:
        function_info = self.config["functions"][function_name]
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

  def is_function_call(self, response, stream):
    if response.get("function_call"): # Check if the response contains a function call
      if self.verbose:
        print(f"Function call: {response['function_call']['name']}({response['function_call']['arguments']})")
      function_name = response["function_call"]["name"]
      function_to_call = self.available_functions[function_name]
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
      if stream:
        self.chat_stream(previous_msgs)
      else:
        self.chat_completion("", previous_msgs)
    else:
      if self.verbose:
        print(f"No function call found.")
      return False

  def chat_stream(self, previous_msgs, prompt=""):
    if previous_msgs == []:
      previous_msgs = [self.system_prompt]
    if prompt != "": # This is so that we can call the completion function without a prompt, for example, when we want to call a function
      previous_msgs.append({"role": "user", "content": prompt})

    stream = self.llm.create_chat_completion(
      model=self.model,
      messages=previous_msgs,
      response_format={"type": "json_object"},
      max_tokens=self.chat_tokens,
      stream=True,
      functions=self.get_functions(),
      function_call=self.function_call,
    )

    function_call_stream = self.is_function_call(next(stream)['choices'][0]['delta'], True)
    if function_call_stream:
      return function_call_stream
    else:
      return stream

  def chat_completion(self, previous_msgs, prompt=""):
    if previous_msgs == []:
      previous_msgs = [self.system_prompt]
    if prompt != "": # This is so that we can call the completion function without a prompt, for example, when we want to call a function
      previous_msgs.append({"role": "user", "content": prompt})

    completion = self.llm.create_chat_completion(
      model=self.model,
      messages=previous_msgs,
      response_format={"type": "json_object"},
      max_tokens=self.chat_tokens,
      functions=self.get_functions(),
      function_call=self.function_call
    )

    function_call_completion = self.is_function_call(completion, False)
    if function_call_completion:
      return function_call_completion
    else:
      return completion