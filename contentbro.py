import os
import logging
import discord
from instagrapi import Client
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import moviepy.editor  # Explicit import to resolve instagrapi dependency
from collections import deque  # Queue for pending uploads

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))
NOTIFICATION_CHANNEL_ID = int(os.getenv("NOTIFICATION_CHANNEL_ID"))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# Set the path for saving temp files
TEMP_DIR = os.path.join(os.getcwd(), "temp_files")
os.makedirs(TEMP_DIR, exist_ok=True)

# Initialize Instagram client once and reuse
insta_client = Client()
try:
    insta_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    logging.info("Instagram login successful")
except Exception as e:
    logging.error(f"Instagram login failed: {e}")

# Queue to store pending video uploads
video_queue = deque()
processing = False  # Track whether the bot is currently processing a video

# Instagram upload function
def upload_to_instagram(video_path, caption):
    try:
        media = insta_client.clip_upload(video_path, caption)
        logging.info("Instagram upload successful!")
        return media
    except Exception as e:
        logging.error(f"Instagram upload error: {e}")
        raise

async def process_queue():
    global processing

    while video_queue:
        processing = True
        message, file_path, caption, message_link = video_queue.popleft()
        
        notification_channel = client.get_channel(NOTIFICATION_CHANNEL_ID)
        if not notification_channel:
            logging.error("Notification channel not found.")
            os.remove(file_path)
            continue

        approval_message = await notification_channel.send(
            f"New video posted [Click to View]({message_link})\nCaption: {caption}\nReact ✅ to approve, ❌ to deny."
        )
        await approval_message.add_reaction("✅")
        await approval_message.add_reaction("❌")

        def check(reaction, user):
            return (
                user != client.user
                and reaction.message.id == approval_message.id
                and str(reaction.emoji) in ["✅", "❌"]
            )

        reaction, user = await client.wait_for("reaction_add", check=check)

        if str(reaction.emoji) == "✅":
            try:
                upload_to_instagram(file_path, caption)
                await notification_channel.send("✅ Video approved and uploaded successfully!")
            except Exception as e:
                await notification_channel.send(f"❌ Error uploading video: {e}")
        else:
            await notification_channel.send("❌ Video denied, not uploaded.")

        os.remove(file_path)

    processing = False  # Finished processing

@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    global processing

    if message.author.bot or message.channel.id != TARGET_CHANNEL_ID:
        return

    for attachment in message.attachments:
        if attachment.content_type and "video" in attachment.content_type:
            file_path = os.path.join(TEMP_DIR, f"temp_{message.id}.mp4")
            await attachment.save(file_path)

            caption = message.content
            message_link = message.jump_url

            # Add video to queue
            video_queue.append((message, file_path, caption, message_link))
            
            # If no videos are currently being processed, start processing
            if not processing:
                await process_queue()

    await client.process_commands(message)

client.run(DISCORD_TOKEN)
