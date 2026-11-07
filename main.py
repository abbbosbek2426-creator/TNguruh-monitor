import os
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION_STRING"]

BOT_TOKEN = os.environ["BOT_TOKEN"]
OWNER_CHAT_ID = os.environ["OWNER_CHAT_ID"]

client = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)

KEYWORDS = [
    "toshkent", "namangan",
    "joy kerak", "mashina kerak",
    "yo'lovchi", "yolovchi",
    "ketaman", "boraman",
    "zayavka", "zakaz",
    "passajir", "место нужно",
    "ищу машину", "такси"
]

@client.on(events.NewMessage(incoming=True))
async def watch_groups(event):
    if not event.is_group:
        return

    message = event.raw_text
    if not message:
        return

    lower = message.lower()

    if not any(word in lower for word in KEYWORDS):
        return

    chat = await event.get_chat()
    title = getattr(chat, "title", "Guruh")

    sender = await event.get_sender()
    sender_name = getattr(sender, "first_name", "Noma'lum")

    text = (
        "🚕 YANGI EHTIMOLIY ZAYAVKA\n\n"
        f"📍 Guruh: {title}\n"
        f"👤 Yuboruvchi: {sender_name}\n\n"
        f"📝 Xabar:\n{message}"
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": OWNER_CHAT_ID,
            "text": text
        },
        timeout=20
    )

async def main():
    await client.start()
    print("TN Guruh Monitor ishga tushdi!")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
