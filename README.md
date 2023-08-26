# PinterestBotDownloader

This Telegram bot allows you to easily upload images and videos from Pinterest to your Telegram chats. Send a Pinterest link to the bot, and it will fetch and send the media content to your chat.

## Requirements

- Python 3.7 or higher
- Install the required libraries using the following command:
  ```bash
  pip install aiogram aiohttp beautifulsoup4
  
Getting Started

    Clone the repository and navigate to the project directory:

    bash

git clone https://github.com/yourusername/pinterest-media-bot.git
cd pinterest-media-bot

Create a .env file in the project directory and add your Telegram bot token:

TELEGRAM_BOT_TOKEN=your_bot_token_here

Run the bot using the following command:

bash

    python PinterestBotDownloader.py 

How to Use

    Start a chat with your Telegram bot.

    Send a Pinterest link to the bot (e.g., https://www.pinterest.com/pin/123456789/).

    The bot will fetch the media content from the Pinterest link and offer you the option to view the original link or the creator's profile link.

    The bot will send the media content as a document to your chat.

Available Commands

    /start: Start a conversation with the bot and receive instructions.

Note

    The bot currently supports direct links to Pinterest images and videos (e.g., https://www.pinterest.com/pin/123456789/). Please ensure that you provide a valid Pinterest link.

    If you encounter any issues or have questions, feel free to open an issue in this repository.

Feel free to contribute to this project by opening pull requests or suggesting improvements. Happy pinning!
