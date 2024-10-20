import os
import asyncio
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import csv

# Function to get input or use environment variable
def get_input_or_env(prompt, env_var):
    value = os.getenv(env_var)
    if not value:
        value = input(prompt)
    return value

# Get sensitive information
api_id = get_input_or_env("Enter your API ID: ", 'TELEGRAM_API_ID')
api_hash = get_input_or_env("Enter your API hash: ", 'TELEGRAM_API_HASH')
phone = get_input_or_env("Enter your phone number (including country code): ", 'TELEGRAM_PHONE')

# Prompt for chat username
chat_username = input("Enter the username of the chat/group/channel: ")

# Use a consistent session name
session_name = 'my_telegram_session'
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    try:
        await client.start()
        
        # Get the chat or channel
        entity = await client.get_entity(chat_username)
        
        # Fetch message history
        messages = await client(GetHistoryRequest(
            peer=entity,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=500,         # Adjust as needed
            max_id=0,
            min_id=0,
            hash=0
        ))
        
        # Open CSV file to write messages
        message_count = 0
        with open('messages.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'User', 'Message'])
            
            for msg in messages.messages:
                if msg.message:
                    writer.writerow([msg.date, msg.sender_id, msg.message])
                    message_count += 1
                # Add a small delay between processing each message
                await asyncio.sleep(0.1)
        
        print(f"Retrieved and saved {message_count} messages to messages.csv")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Add a delay before the next run
        print("Waiting for 60 seconds before the next run...")
        time.sleep(60)

# Running the client
with client:
    client.loop.run_until_complete(main())