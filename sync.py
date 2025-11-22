import os
from telethon import TelegramClient, events

# اخد البيانات من Environment Variables
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

# IDs الجروب والقناة (هتحطهم بعد ما تجيبهم)
source_chat = int(os.environ.get("SOURCE_CHAT"))
target_channel = int(os.environ.get("TARGET_CHANNEL"))

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=source_chat))
async def handler(event):
    msg = event.message
    try:
        if msg.media:
            await client.send_file(target_channel, msg.media, caption=msg.text or "")
        else:
            await client.send_message(target_channel, msg.text or "")
    except Exception as e:
        print("Error:", e)

client.start()
print("Bot is running...")
client.run_until_disconnected()
