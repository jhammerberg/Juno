from llama_cpp import Llama

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = Llama(
  model_path="./dolphin-2.5-mixtral-8x7b.Q4_K_M.gguf",  # Download the model file first
  n_ctx=int((32768)/2),            # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=0         # The number of layers to offload to GPU, if you have GPU acceleration available
)

# Simple inference example
output = llm('''
             <|im_start|>system\n
             {system_message}
             <|im_end|>\n
             <|im_start|>user\n
             {prompt}
             <|im_end|>\n
             <|im_start|>
             assistant
             ''',
  max_tokens=512,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=True        # Whether to echo the prompt
)

# Chat Completion API

llm = Llama(model_path="./dolphin-2.5-mixtral-8x7b.Q4_K_M.gguf", chat_format="llama-2")  # Set chat_format according to the model you are using
llm.create_chat_completion(
    messages = [
        {"role": "system", "content": "You are a story writing assistant."},
        {
            "role": "user",
            "content": "Write a story about llamas."
        }
    ]
)