import os
import asyncio
from telethon import TelegramClient, events

# Load credentials from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
source_channel = int(os.environ['SOURCE_CHANNEL'])
destination_channel = int(os.environ['DESTINATION_CHANNEL'])

# Initialize the client
client = TelegramClient('user_session', api_id, api_hash)

# Event handler for new messages
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        message = event.message
        media_files = []

        if message.media:
            file_path = await message.download_media(file="downloads/")
            media_files.append(file_path)

            if message.document:
                mime_type = message.document.mime_type
                if mime_type.startswith("audio/"):
                    print(f"Audio detected: {file_path}")
                elif mime_type.startswith("video/"):
                    print(f"Video detected: {file_path}")

        if message.grouped_id:
            await client.send_file(destination_channel, media_files, caption=message.text or "")
            print("Album (multiple media) forwarded successfully.")
        elif media_files:
            await client.send_file(destination_channel, media_files[0], caption=message.text or "")
            print(f"Media forwarded successfully: {media_files[0]}")
        else:
            await client.send_message(destination_channel, message.text or "")
            print("Text message forwarded successfully.")

        for file in media_files:
            await asyncio.sleep(1)
            os.remove(file)

    except Exception as e:
        print(f"Error: {e}")

# Start the client
print("Logging in with your account...")
client.start()
print("Listening for new messages from the source channel...")
client.run_until_disconnected()
