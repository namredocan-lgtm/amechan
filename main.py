import discord
import asyncio
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError

# === CONFIG ===
DISCORD_TOKEN = "MTQwOTU0NTMwNDE1NTYxOTQwOQ.Gw5bzy.iCUHIAsq3C3lxfN1OwbefxW7xHSX0dsvC6wixM"   # <-- replace with your bot token
CAI_TOKEN = "59d12e7bb8a03e4afc64ee267d2ef5aa12e14f34"
CHARACTER_ID = "yR-BB03I0cV75kPajA7xmOpkngAAxMcwAslUGv0eAdE"

# === Discord Bot Setup ===
intents = discord.Intents.default()
intents.message_content = True  # needed for reading messages
client = discord.Client(intents=intents)

# === Character.AI Setup ===
cai_client = None
chat = None

@client.event
async def on_ready():
    global cai_client, chat
    cai_client = await get_client(token=CAI_TOKEN)
    me = await cai_client.account.fetch_me()
    chat, greeting_message = await cai_client.chat.create_chat(CHARACTER_ID)

    print(f"✅ Logged in as {client.user}")
    print(f"🤖 Connected to Character.AI as @{me.username}")
    print(f"💬 Greeting: {greeting_message.get_primary_candidate().text}")

@client.event
async def on_message(message):
    global chat
    if message.author == client.user:
        return  # ignore the bot's own messages

    try:
        # Send user message to Character.AI
        response = await cai_client.chat.send_message(
            CHARACTER_ID, chat.chat_id, message.content
        )
        # Reply ONLY with the text (no author name)
        await message.channel.send(response.get_primary_candidate().text)

    except SessionClosedError:
        await message.channel.send("⚠️ Session closed. Please restart the bot.")

@client.event
async def on_disconnect():
    if cai_client:
        await cai_client.close_session()

client.run(DISCORD_TOKEN)
