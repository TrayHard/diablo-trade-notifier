import asyncio
import websockets
import requests
import json
import sys
import os.path

from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_RECIP_ID = os.getenv('RECIPIENT_TG_ID')
PLATFORM = os.getenv('PLATFORM')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'
TOKENS_FILE_PATH='./tokens.txt'

connect_string=""
subscribe_string=""

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_telegram_message(message):
    payload = {
        'chat_id': TG_RECIP_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message to telegram: {response.text}")

# def send_discord_message(message):
#     print(message)

def escape_markdown(text):
    return text.replace('_', r'\_').replace('*', r'\*').replace('[', r'\[').replace(']', r'\]').replace('`', r'\`')

def notify_dm(sender, message_content, platform=PLATFORM):
    if (platform == 'telegram'):
        processed_message = escape_markdown(message_content)
        send_telegram_message(f"*Diablo Trade*\n\n*{sender}:*\n**{processed_message}**\n\n🔗__https://diablo.trade/chat__")
#     if (platform == 'discord')
#         send_discord_message(message_content)

def notify_status(message, platform=PLATFORM):
    if (platform == 'telegram'):
        send_telegram_message(message)
#     if (platform == 'discord')
#         send_discord_message(message)

def get_line_from_file(file_path, line_number=1):
    try:
        with open(file_path, 'r') as file:
            for current_line_number, line in enumerate(file, start=1):
                if current_line_number == line_number:
                    return line.strip()
        raise ValueError()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        raise ValueError()

async def connect():
    ws_uri="wss://sockets.diablo.trade/connection/websocket"
    while True:
        try:
            async with websockets.connect(ws_uri) as websocket:
                await websocket.send(connect_string)
                print(f"[{get_timestamp()}]: Connecting...")
                response = json.loads(await websocket.recv())
                print(f"[{get_timestamp()}]: Recieved: {response}")
                if 'error' in response:
                    notify_status(f'*Diablo Trade*\n\n🚫 Error: { response["error"]["message"] }', PLATFORM)
                    print(response["error"])
                    return

                await websocket.send(subscribe_string)
                print(f"[{get_timestamp()}]: Subscribing...")
                response = await websocket.recv()
                print(f"[{get_timestamp()}]: Recieved: {response}")

                while True:
                    response = await websocket.recv()

                    if response == "{}":
                        await websocket.send("{}")
                        sys.stdout.write(f"\rLast handshake was at [{get_timestamp()}]")
                        sys.stdout.flush()

                    else:
                        try:
                            data = json.loads(response)
                            if data["push"]["pub"]["data"]["type"] != "R_MESSAGE":
                                continue

                            message_content = data["push"]["pub"]["data"]["body"]["payload"]["message"]["content"]
                            sender = data["push"]["pub"]["data"]["body"]["payload"]["message"]["sender"]

                            notify_dm(sender, message_content, 'telegram')
                        except (KeyError, json.JSONDecodeError) as e:
                            print(f"[{get_timestamp()}]: Failed to parse response: {e}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"[{get_timestamp()}] - WS connection closed: {e}")

def process_token_file(file_path=TOKENS_FILE_PATH):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass
        print(f"Tokens file created at {file_path}.")
        raise ValueError("Please add required lines to ./tokens.txt. Check README.md if you don't know how.")
    else:
        print(f"Tokens file already exists at {file_path}")
        global connect_string
        global subscribe_string
        try:
            connect_string=get_line_from_file(TOKENS_FILE_PATH, 1)
            subscribe_string=get_line_from_file(TOKENS_FILE_PATH, 2)
            return True
        except:
            raise ValueError("Please add required lines to ./tokens.txt. Check README.md if you don't know how.")

def start():
    process_token_file(TOKENS_FILE_PATH)
    asyncio.run(connect())

if __name__ == "__main__":
    start()
