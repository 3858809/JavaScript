import os
import time
import asyncio
import base64
import json
import re
import requests

from telethon import TelegramClient, events, sync

api_id = [5672799]	#输入api_id，一个账号一项
api_hash = ['e08529171140eac69071c630f03f1a7a']	#输入api_hash，一个账号一项

robot_map = {'@blueseamusic_bot':'/checkin'}
session_name = api_id[:]
print("开始签到")

for num in range(len(api_id)):
	session_name[num] = "id_" + str(session_name[num])
	client = TelegramClient(session_name[num], api_id[num], api_hash[num])
	client.start()
	
	for (k,v) in robot_map.items():
		client.send_message(k, v) #设置机器人和签到命令
		time.sleep(3)
		@client.on(events.NewMessage(chats=k))
		async def handler(event):
			print("当前签到机器人:", k)
			# 获取带按钮的消息
			print("获取的信息: ", event.message.text)
			if "您距离下次可签到时间还剩" in event.message.text or "已经签到过了" in event.message.text:
				print("已经签到过了")
			elif "请输入验证码" in event.message.text:
				print("开始处理验证码签到!")
				print("开始下载图片!")
				path = await client.download_profile_photo('BlueSeaSupportsBot')
				print(path)
				print("path:",path)
				print("下载图片完毕!")
				# 使用 TRUECAPTCHA 模块解析验证码
				solved_result = captcha_solver("captcha.jpg")
				if not "result" in solved_result:
					client.send_message(CHANNEL_ID, "21342")
					return
				captcha_code = handle_captcha_solved_result(solved_result)
				client.send_message(event.message.chat_id, captcha_code)
				# 删除临时文件
				os.remove("captcha.jpg")

		client.send_read_acknowledge(k)	#将机器人回应设为已读
		client.disconnect()
	print("Done! Session name:", session_name[num])		
os._exit(0)
