import asyncio
import base64
import json
import os
import re
import requests
from telethon import TelegramClient, events, sync

def yzm(mc):
	print("开始识别验证码图片")
  # 使用 TRUECAPTCHA 模块解析验证码
  solved_result = captcha_solver("captcha.jpg")
  if not "result" in solved_result:
    await client.send_message(CHANNEL_ID, "21342")
    return
  captcha_code = handle_captcha_solved_result(solved_result)
  await client.send_message(event.message.chat_id, captcha_code)
  # 删除临时文件
	return jg


result = yzm('captcha.jpg')

os._exit(0)
