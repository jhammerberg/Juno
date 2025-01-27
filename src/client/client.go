package client

import (
	"fmt"
	"log"
	"os"
	"strings"

	"juno/src/ai"

	"github.com/bwmarrin/discordgo"
	"github.com/joho/godotenv"
)

func messageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {
	// Ignore all messages created by the bot itself
	if m.Author.ID == s.State.User.ID {
		return
	}
	// see if the message contains any version of the string "juno"
	if strings.Contains(strings.ToLower(m.Content), "juno") {
		s.ChannelTyping(m.ChannelID)
		//time.Sleep(2 * time.Second)
		s.ChannelMessageSend(m.ChannelID, ai.GenerateResponse(m.Content))
	}
}

func Run() {
	log.Println("Loading the model")
	ai.Init()
	log.Println("Model loaded successfully")

	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file for bot credentials")
	}
	discord_key := os.Getenv("DISCORD_KEY")

	bot, err := discordgo.New("Bot " + discord_key)
	if err != nil {
		log.Fatal("Could not authenticate with provided credentials")
	}

	err = bot.Open()
	if err != nil {
		log.Fatal("Error opening connection to Discord")
	}
	defer bot.Close()

	bot.UpdateGameStatus(0, "Deepseek R-1")

	bot.AddHandler(messageCreate)

	fmt.Println("Bot is now running. Press CTRL+C to exit.")
	select {}
}
