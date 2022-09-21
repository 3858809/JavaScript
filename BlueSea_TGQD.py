import os
import time
import asyncio
import base64
import json
import re
import requests

from telethon import TelegramClient, events, sync

api_id = 5672799	#输入api_id，一个账号一项
api_hash = 'e08529171140eac69071c630f03f1a7a'	#输入api_hash，一个账号一项

i = 0

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

async def main():
	MSG = '/checkin'
	CHANNEL_ID = '@blueseamusic_bot'
	async with TelegramClient("CLIENT_NAME", api_id, api_hash) as client:
		await client.send_message(CHANNEL_ID, MSG)
		time.sleep(3)
		@client.on(events.NewMessage(chats=CHANNEL_ID))
		async def handler(event):
			global i
			print("获取的信息: ", event.message.text)
			if "您距离下次可签到时间还剩" in event.message.text or "已经签到过了" in event.message.text:
				print("已经签到过了")
				i = 1
			elif "请输入验证码" in event.message.text:  # 获取图像验证码
				print("开始处理验证码签到!")
				print("开始下载")
				await client.download_media(event.message.photo, "captcha.jpg")
				time.sleep(5)
				print("下载完毕!")
				# 使用 TRUECAPTCHA 模块解析验证码
				solved_result = captcha_solver("captcha.jpg")
				print("solved_result=",solved_result)
				await client.send_message(event.message.chat_id, solved_result)
				# 删除临时文件
				os.remove("captcha.jpg")
		await client.send_read_acknowledge(CHANNEL_ID)	#将机器人回应设为已读
		await client.disconnect()

while i == 0:
	asyncio.run(main())
