# Juno AI 

Juno is an AI platform or framework built on Ollama for deploying AI models for Discord servers (it's original purpose) but can also be used for other projects. This project originally started as an OpenAI interface for Discord, then transformed into a local AI framework built with Python, this current rewrite is in Go and uses Ollama to streamline the process of integrating vector databases and different AI models. The most recent rewrite was inspired by the release of Deepseek R-1 but you can use other models as well.

## Usage

### Requirements

- Go 1.23 or higher
- The packages used (should be installed automatically when you build)
- Ollama
- A model that is compatible with Ollama
    - Install Deepseek R-1 with `Ollama pull deepseek-r1`
    - If you plan on using a model different than Deepseek R-1 you will need to modify the code slightly in `src/ai.go`

### Build and Run

For the discord client example:

```bash
go build -o src/main.go
```

or 

```bash
go run src/main.go
```

## Planned features
- YAML config file
- Automatic model installation
- Function calling
- Vector database for long-term memory
- Embedding usernames into AI calls
- Voice recognition / voice-call integration

## License
Feel free to use an modify this code as you see fit for any purpose. The only restriction is that you cannot claim the original code as your own. It would also be nice if you could credit me if you use this code in a project.