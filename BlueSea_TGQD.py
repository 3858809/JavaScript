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
channel_link = "blueseamusic_bot"
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

def HQXX():
	for message in client.iter_messages(channel_link):
		return message.text
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
while 1==1:
	time.sleep(2)
	newmeg = HQXX()
	print("获取的新信息=",newmeg)
	if newmeg == '/checkin':
		client.send_message(channel_link,"/cancel")
		time.sleep(1)
		client.send_message(channel_link, QDmeg) #发送签到命令
	elif "签到验证码" in  newmeg:
		XZYZM()#下载验证码图片
		YZM = captcha_solver(channel_link + "/YZM.jpg")
		print("发送验证码=",YZM) 
		client.send_message(channel_link, YZM) #发送签到验证码
		time.sleep(3)
	elif "今天已签过到" in newmeg or "签到成功" in newmeg:
		print("已经签到过")
		break
	else:
		client.send_message(channel_link, QDmeg) #发送签到验证码

client.send_read_acknowledge(channel_link) #将机器人回应设为已读
client.disconnect()
print("脚本结束")
