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

robot_map = {'@EmbyMistyBot':'⚡️注册账号'}

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
	MSG = '⚡️注册账号'
    CHANNEL_ID = '@EmbyMistyBot'
    async with TelegramClient("CLIENT_NAME", api_id, api_hash) as client:
        await client.send_message(CHANNEL_ID, MSG)
        time.sleep(3)
        @client.on(events.NewMessage(chats=CHANNEL_ID))
        async def handler(event):
			print("当前获取对象:", k)
			print("本次为第", i,"次获取信息")
			# 获取带按钮的消息
			print("获取的信息: ", event.message.text)
			
			if "您距离下次可签到时间还剩" in event.message.text or "已经签到过了" in event.message.text:
				print("已经签到过了")
				i += 100
			elif d > 0:
				print("上一条处理还没有结束!")
			elif "请输入验证码" in event.message.text:  # 获取图像验证码
				print("开始处理验证码签到!")
				print("开始下载")
				d = 1
				await client.download_media(event.message.photo, "captcha.jpg")
				print("下载完毕!")
				# 使用 TRUECAPTCHA 模块解析验证码
				solved_result = captcha_solver("captcha.jpg")
				print("solved_result=",solved_result)
				await client.send_message(k, solved_result)
				# 删除临时文件
				os.remove("captcha.jpg")
				d = 0
			elif event.message.buttons:
				print("发现按钮信息")
				# 匹配按钮文本并点击
				for button in event.message.buttons[0]:
					if '点击抢注册' in button.text or '红包' in button.text:
						print("匹配按钮文本成功点击按钮")
						await button.click()
							break

		await client.send_read_acknowledge(k)	#将机器人回应设为已读
		
	await client.disconnect()

asyncio.run(main())
