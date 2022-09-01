import os
import time
import asyncio
import base64
import json
import re
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
			elif event.message.buttons:
				# 获取算式 卷毛鼠
				# '请回答下面的问题：\n32 處以 4 = ? (请在60秒内回答)'
				formula = ""
				if k == "@qweybgbot":
					formula = event.message.raw_text.split('\n')[1]  #处理卷毛鼠签到格式
				elif k == "@EmbyPublicBot":
					formula = event.message.raw_text.split('\n\n')[1]  #处理终点站签到格式
				# 计算结果 25 + 1 = ?
				js = formula.split(' ')[1]
				print("计算符号:", js)
				result = int(formula.split(' ')[0]) + int(formula.split(' ')[2])
				if "加" == js or "+" == js or "加以" == js or "枷" == js:
					result = int(formula.split(' ')[0]) + int(formula.split(' ')[2])
				elif "减" == js or "-" == js or "缄" == js:
					result = int(formula.split(' ')[0]) - int(formula.split(' ')[2])
				elif "乘" == js or "*" == js or "乗以" == js or "騬以" == js or "×" == js:
					result = int(formula.split(' ')[0]) * int(formula.split(' ')[2])
				elif "除" == js or "/" == js or "除以" == js or "處以" == js:
					result = int(formula.split(' ')[0]) / int(formula.split(' ')[2])
				print("计算结果:", result)
				# 匹配按钮文本并点击
				for button in event.message.buttons[0]:
					if int(button.text) == result:
						await button.click()
						break
			elif "请输入验证码" in event.message.text:  # 获取图像验证码
				print("验证码签到机制")
				print("获取图片:",event.message.photo)
				print("获取image_base:",event.message.media)
				image_base = event.message.media
				print("获取image_bytes:",image_base.photo.bytes)
				image_bytes = image_base.photo.bytes
				await client.download_media(image_bytes, "captcha1.jpg")
				await client.download_media(event.message.photo, "captcha.jpg")
				print("下载验证码图片完毕")
				# 使用 TRUECAPTCHA 模块解析验证码
				solved_result = captcha_solver("captcha.jpg")
				print("使用 TRUECAPTCHA 模块解析验证码完毕:",solved_result)
				if not "result" in solved_result:
					await client.send_message(k, "21342")
					return
				print("开始获取验证码")
				captcha_code = handle_captcha_solved_result(solved_result)
				print("获取验证码:",captcha_code)
				await client.send_message(event.message.chat_id, captcha_code)
				# 删除临时文件
				print("删除临时文件")
				os.remove("captcha.jpg")
		
		client.send_read_acknowledge(k)	#将机器人回应设为已读
		client.disconnect()
	print("Done! Session name:", session_name[num])		
os._exit(0)
