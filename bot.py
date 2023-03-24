import os
import io
import openai
import httpx
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Get your environment variables for OpenAI API key and Discord bot token
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

DALLE_API_URL = "https://api.openai.com/v1/images/generations"

# Set up the bot
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Set up logging
logging.basicConfig(level=logging.ERROR, filename="error.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    activity = discord.Activity(type=discord.ActivityType.listening, name="!ask or !image")
    await bot.change_presence(activity=activity)

@bot.command(name="name", help="Returns the bot's name.")
async def name(ctx):
    try:
        await ctx.send("My name is Starrie.")
    except Exception as e:
        print(f"Error in name command: {e}")
        await on_command_error(ctx, e)

async def generate_text(messages):
    headers = {"Authorization": f"Bearer {openai.api_key}"}
    data = {"model": "gpt-3.5-turbo", "messages": messages}
    url = "https://api.openai.com/v1/chat/completions"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"Error generating text: {response.status_code}")
            return "I'm sorry, I couldn't generate a response."
    except Exception as e:
        print(f"Error in generating text: {e}")
        return "I'm sorry, I couldn't generate a response."

@bot.command(name="ask", help="Ask Starrie anything.")
async def ask(ctx, *, question):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
        response = await generate_text(messages)
        await ctx.send(response)
    except Exception as e:
        print(f"Error in ask command: {e}")
        await on_command_error(ctx, e)

async def generate_image(prompt, n=1, size="512x512"):
    headers = {"Authorization": f"Bearer {openai.api_key}"}
    data = {"prompt": prompt, "n": n, "size": size}

    async with httpx.AsyncClient() as client:
        response = await client.post(DALLE_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["data"][0]["url"]
    else:
        print(f"Error generating image: {response.status_code}")
        return None

@bot.command(name="image", help="Generate an image with DALL-E.")
async def image(ctx, *, prompt):
    try:
        image_url = await generate_image(prompt)
        if image_url:
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)

            if response.status_code == 200:
                image_bytes = io.BytesIO(response.content)
                image_file = discord.File(image_bytes, "image.png")
                await ctx.send(file=image_file)
            else:
                await ctx.send("I'm sorry, I couldn't download the image.")
        else:
            await ctx.send("I'm sorry, I couldn't generate an image.")
    except Exception as e:
        print(f"Error in image command: {e}")
        await on_command_error(ctx, e)

@bot.command(name="help", help="Displays the available commands and their explanations.")
async def help_command(ctx):
    try:
        help_text = """
        Available commands:

        !ask [question] - Ask Starrie anything.
        !image [prompt] - Generate an AI image based on the prompt.
        !help - Displays the available commands and their explanations.

        To use a command, simply type it with the required parameters. For example: !ask What is the capital of France?
        """
        await ctx.send(help_text.strip())
    except Exception as e:
        print(f"Error in help command: {e}")
        await on_command_error(ctx, e)

@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Command '{ctx.message.content}' caused an error: {error}")
    await ctx.send("I'm sorry, something went wrong. The error has been logged.")

bot.run(TOKEN)
