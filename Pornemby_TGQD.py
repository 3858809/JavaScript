import os
import time
from telethon.sync import TelegramClient


api_id = 5672799	#输入api_id，一个账号一项
api_hash = 'e08529171140eac69071c630f03f1a7a'	#输入api_hash，一个账号一项

name = 'CLIENT_NAME'

with TelegramClient(name, api_id, api_hash) as client:
    for message in client.iter_messages(chat):
        print(message.sender_id, ':', message.text)