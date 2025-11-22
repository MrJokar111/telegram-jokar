import os
from telethon import TelegramClient, events

# اخد البيانات من Environment Variables
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH"))

source_chat = int(os.environ.get("SOURCE_CHAT"))
target_channel = int(os.environ.get("TARGET_CHANNEL"))

client = TelegramClient('bot', api_id, api_hash).start(bot_token=os.environ.get("BOT_TOKEN"))

@client.on(events.NewMessage(chats=source_chat))
async def handler(event):
    msg = event.message
    try:
        if msg.media:
            caption = msg.text if msg.text else None
            await client.send_file(target_channel, msg.media, caption=caption)
        elif msg.text:
            await client.send_message(target_channel, msg.text)
    except Exception as e:
        print("Error:", e)

print("Bot is running...")
client.run_until_disconnected()
