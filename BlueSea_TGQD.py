import asyncio
import base64
import json
import os
import re
import requests
from telethon import TelegramClient, events

API_ID = 5672799	#输入api_id，一个账号一项
API_HASH = 'e08529171140eac69071c630f03f1a7a'	#输入api_hash，一个账号一项

async def main():
	MSG = '/checkin'
	CHANNEL_ID = '@blueseamusic_bot'
	print("开始签到!签到对象:",CHANNEL_ID)
	async with TelegramClient("CLIENT_NAME", API_ID, API_HASH) as client:
		await client.send_message(CHANNEL_ID, MSG)
		@client.on(events.NewMessage(chats=CHANNEL_ID))
		async def handler(event):
			# 根据button count 区分消息类型
			if "签到成功" in event.message.text or "上次签到" in event.message.text:
				print("签到成功")
				# 结束异步任务
				await client.disconnect()
			elif event.message.buttons:
				if event.message.button_count == 6:  # 主菜单
					await event.message.buttons[2][0].click()
				elif event.message.button_count == 7:  # 更多功能
					await event.message.buttons[0][1].click()
				# 图像验证码处理
			elif "请输入验证码" in event.message.text:  # 获取图像验证码
				await client.download_media(event.message.photo, "captcha.jpg")
				# 使用 TRUECAPTCHA 模块解析验证码
				solved_result = captcha_solver("captcha.jpg")
				if not "result" in solved_result:
					await client.send_message(CHANNEL_ID, "21342")
					return
				captcha_code = handle_captcha_solved_result(solved_result)
				await client.send_message(event.message.chat_id, captcha_code)
				# 删除临时文件
				os.remove("captcha.jpg")
			elif "已签过到" in event.message.text:  # 已经签到过
				print("已签过到")
			# 是否成功签到
			elif "验证码错误" in event.message.text:
				await client.send_message(event.message.chat_id, RETURE_MENU)
asyncio.run(main())
