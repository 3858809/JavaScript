import asyncio
import base64
import json
import os
import re
import requests
import time

from telethon import TelegramClient, events

API_ID = 5672799	#输入api_id，一个账号一项
API_HASH = 'e08529171140eac69071c630f03f1a7a'	#输入api_hash，一个账号一项

async def main():
	MSG = '⚡️注册账号'
	CHANNEL_ID = '@EmbyMistyBot'
	print("开始签到!签到对象:",CHANNEL_ID)
	async with TelegramClient("CLIENT_NAME", API_ID, API_HASH) as client:
		await client.send_message(CHANNEL_ID, MSG)
		time.sleep(5)
		@client.on(events.NewMessage(chats=CHANNEL_ID))
		async def handler(event):
			# 根据button count 区分消息类型
			print("获取的信息:",event.message.text)
			if "签到成功" in event.message.text or "上次签到" in event.message.text:
				print("签到成功")
				# 结束异步任务
				await client.disconnect()
			elif "请输入验证码" in event.message.text:  # 获取图像验证码
				print("开始处理验证码签到!")
				print("开始下载")
				path = await events.message.download_media()
				print("下载完毕!",path)
				# 使用 TRUECAPTCHA 模块解析验证码
				#solved_result = captcha_solver("captcha.jpg")
				#if not "result" in solved_result:
				#	await client.send_message(CHANNEL_ID, "21342")
				#	return
				#captcha_code = handle_captcha_solved_result(solved_result)
				#await client.send_message(event.message.chat_id, captcha_code)
				# 删除临时文件
				#os.remove("captcha.jpg")
			elif "已签过到" in event.message.text:  # 已经签到过
				print("已签过到")
			# 是否成功签到
			elif "验证码错误" in event.message.text:
				await client.send_message(event.message.chat_id, RETURE_MENU)
asyncio.run(main())
