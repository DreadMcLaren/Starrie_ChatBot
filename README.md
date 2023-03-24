# Installation Instructions

**NOTE:** This install guide was created using linux Ubuntu and assumes you've already created your bot and obtained your Discord token and OpenAI API key. Make sure to navigate to "Privileged Gateway Intents" section and enable "Server Members Intent" and "Message Content Intent" at [Discord's Developer Portal](https://discord.com/developers/applications).

1. SSH into server
```
ssh USERNAME@IP-ADDRESS
```

2. Update the server
```
sudo apt-get update && sudo apt-get upgrade -y
```

3. Install Python, Pip, Git and Screen
```
sudo apt-get install python3 python3-pip screen git -y
```

4. Install bot dependencies
```
pip3 install discord.py openai httpx python-dotenv
```

5. Clone the repository
```
git clone https://github.com/DreadMcLaren/Starrie_Chatbot.git
```

6. Navigate to where you saved it
```
cd path/to/bot
```

7. Open the ```.env``` file
```
nano .env
```

Add your Discord token, OpenAI API key and desired password. Save it ```CTRL + X``` and ```Y``` keeping the same file name
```
DISCORD_BOT_TOKEN=Your_Discord_Token
OPENAI_API_KEY=Your_OpenAI_Key
```

8. Start the bot

```
python3 bot.py
```

**The bot will now be running and listening for messages on Discord. The log file (```error.log```) will be placed in the same directory your bot is in.**

To answer questions, use ```!ask``` followed by your prompt.

To generate an image with DALLE AI, use ```!image``` followed by your prompt.

Example:

```
!ask What is the size of the moon?
!image a white siamese cat
```

--------------------------------------------
**OPTIONAL:**

You can run the bot in a detatch state using Screen.

```
cd path/to/bot
```

```
screen -S bot-session
```

```
python3 bot.py
```

To detatch from the running bot, press ```Ctrl + A``` followed by ```D```
