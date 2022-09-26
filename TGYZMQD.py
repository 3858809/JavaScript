import os
import time
import asyncio
import base64
import json
import re
import requests

from telethon import TelegramClient,sync
from telethon.tl.types import InputMessagesFilterPhotos
proxy = None
# =============需要被替换的值=================
'''
api_id 你的api id
api_hash 你的api hash
channel_link 要下载图片的频道链接
proxy 将localhost改成代理地址,12345改成代理端口
picture_storage_path 图片下载到的路径
'''
api_id = 5672799
api_hash = "e08529171140eac69071c630f03f1a7a"
channel_link = "EmbyPublicBot"
QDmeg = "/checkin"
#proxy =("socks5","localhost",12345) #不需要代理的话删掉该行
# ==========================================
client = TelegramClient('shexiaoyu',api_id=api_id,api_hash=api_hash,proxy=proxy).start()

#下载验证码图片
def XZYZM():
	photos = client.get_messages(channel_link, None, filter=InputMessagesFilterPhotos)
	index = 0
	for photo in photos:
		filename = channel_link + "/YZM.jpg"
		index = index + 1
		if index == 1:
			client.download_media(photo, filename)
		break
	print("下载完毕")

def HQXX()
	channel_username='EmbyPublicBot' # your channel
	channel_entity=client.get_entity(channel_username)
	posts = client(GetHistoryRequest(
	peer=channel_entity,
	limit=100,
	offset_date=None,
	offset_id=0,
	max_id=0,
	min_id=0,
	add_offset=0,
	hash=0))
	for meg in posts.messages:
		print(meg)
	
def captcha_solver(f):
	with open(f, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read()).decode('ascii')
		url = 'https://api.apitruecaptcha.org/one/gettext'
		data = { 
			'userid':'sheriqiang@gmail.com', 
			'apikey':'L7GYXVaB2BreQrGhzh3I',  
			'data':encoded_string
		}
		response = requests.post(url = url, json = data)
		data = response.json()
		return data['result']
	
client.send_message(channel_link, QDmeg) #发送签到命令
time.sleep(1)
XZYZM()#下载验证码图片
time.sleep(2)
YZM = captcha_solver(channel_link + "/YZM.jpg")
print("识别的验证码=",YZM)
HQXX()
#client.send_message(channel_link, YZM) #发送签到验证码

client.disconnect()
print("脚本结束")
