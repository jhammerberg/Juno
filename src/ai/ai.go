package ai

import (
	"context"
	"fmt"
	"log"
	"strings"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/ollama"
)

var (
	llm     llms.Model
	ctx     context.Context
	history []llms.MessageContent
)

func Init() {
	var err error
	llm, err = ollama.New(
		ollama.WithModel("deepseek-r1"),
		// ollama.WithSystemPrompt("You are Juno"),
		//ollama.WithKeepAlive("5m"), // five minutes, idk why they pass it as a string lmao
	)
	if err != nil {
		log.Fatal("Init failure: ", err)
	}
	if ctx == nil { // only make a fresh context window if one does not already exist
		ctx = context.Background()
	}
	if history == nil {
		history = []llms.MessageContent{
			llms.TextParts(llms.ChatMessageTypeAI, "<think> I am Juno, an artificial intelligence system created by the engineer Jack Hammerberg. I should respond as my creator intends by being witty, clever, and ocassionally sarcastic. I should always respond to myself in the first person and I should always think of myself as an artificial intellegence. </think>"),
		}
	}
}

func extractResponse(content *llms.ContentResponse) string {
	response := content.Choices[0].Content
	// take just the section after the ending </think> (if that exists)
	if response != "" {
		thinkIndex := strings.LastIndex(response, "</think>")
		if thinkIndex != -1 {
			response = response[thinkIndex+len("</think>"):]
		}
	}

	return response
}

func GenerateResponse(message string) string {
	if llm == nil {
		Init() // Check if the model has been unloaded for inactivity
	}
	if message == "" {
		return ""
	} else {
		content := llms.TextParts(llms.ChatMessageTypeHuman, message)
		history = append(history, content)
	}

	completion, err := llm.GenerateContent(ctx, history)
	if err != nil {
		log.Fatal("GenerateContent failure: ", err)
	}
	// add the completion to the history
	history = append(history, llms.TextParts(llms.ChatMessageTypeAI, completion.Choices[0].Content))

	fmt.Println("Response: ", completion.Choices[0].Content)
	return extractResponse(completion)
}
