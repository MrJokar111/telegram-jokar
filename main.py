import os
from telethon import TelegramClient, events, types

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN"))

source_chat = int(os.environ.get("SOURCE_CHAT"))
target_channel = int(os.environ.get("TARGET_CHANNEL"))

client = TelegramClient('bot', api_id, api_hash)


message_map = {}

async def start_bot():
    await client.start(bot_token=bot_token)
    print("Bot started successfully!")

@client.on(events.NewMessage(chats=source_chat))
async def new_message_handler(event):
    msg = event.message
    try:
        reply_to = None

        if msg.is_reply and msg.reply_to_msg_id in message_map:
            reply_to = message_map[msg.reply_to_msg_id]

        if msg.media:
            caption = msg.text if msg.text else None
            sent_msg = await client.send_file(target_channel, msg.media, caption=caption, reply_to=reply_to)
        elif msg.text:
            sent_msg = await client.send_message(target_channel, msg.text, reply_to=reply_to)
        else:
            return


        message_map[msg.id] = sent_msg.id

    except Exception as e:
        print("Error:", e)

@client.on(events.MessageEdited(chats=source_chat))
async def edited_message_handler(event):
    msg = event.message
    try:

        if msg.id in message_map:
            target_msg_id = message_map[msg.id]
            if msg.text:
                await client.edit_message(target_channel, target_msg_id, msg.text)

    except Exception as e:
        print("Edit Error:", e)

with client:
    client.loop.run_until_complete(start_bot())
    client.run_until_disconnected()
