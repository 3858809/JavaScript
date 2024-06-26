import os
import time
import re
import requests
import asyncio
import base64
import json

from telethon import TelegramClient, events, sync

api_id = [5672799]	#输入api_id，一个账号一项
api_hash = ['e08529171140eac69071c630f03f1a7a']	#输入api_hash，一个账号一项

qdcode=input（"请输入准备好的抢注验证码:"）

robot_map = {'FreeEmby':'/checkin'}
session_name = api_id[:]

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

def GetWXMeg(text):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	data = { 
		'appToken':'AT_OdRi5Z4hzWMr225NfPVHhXVSmfN59GeR', 
		'content':text,  
		'summary':'抢注册监听提醒',
		'contentType':1,
		'uids':['UID_8krNXTxaevo6ogJ1g1W3wTnhZpZR'],
		'url':'https%3A%2F%2Fpornemby.club%2Fweb%2Findex.html'
	}
	response = requests.post(url = url, json = data)
	data = response.json()
	return 'ok'

for num in range(len(api_id)):
	session_name[num] = "id_" + str(session_name[num])
	client = TelegramClient(session_name[num], api_id[num], api_hash[num])
	client.start()
	
	#for dialog in client.iter_dialogs():
	#	print(dialog.name, 'has ID', dialog.id)
	
	for (k,v) in robot_map.items():
		i = 0
		n = 0
		while i<9000000:
			i += 1
			#client.send_message(k, v) #设置机器人和签到命令
			print("正在获取新消息",i)
			time.sleep(2)
			@client.on(events.NewMessage(chats=k))
			async def handler(event):
				global i
				global n
				time.sleep(1)
				print("当前获取对象:", k)
				print("本次为第", i,"次获取信息")
				# 获取带按钮的消息
				print("获取的信息: ", event.message.text)
				if i > 50 :
					n = 0
				else:
					n = 1
				if "您距离下次可签到时间还剩" in event.message.text or "已经签到过了" in event.message.text:
					print("已经签到过了")
					i += 100
				elif "空余名额数" in event.message.text:
					if n==0:
						i = 0
						n = 1
						GetWXMeg(event.message.text)
						if "空余名额数: 0" not in  event.message.text:
							client.send_message(k,qdcode)
				elif event.message.buttons:
					print("发现按钮信息")
					# 匹配按钮文本并点击
					for button in event.message.buttons[0]:
						if '点击抢注册' in button.text or '红包' in button.text:
							print("匹配按钮文本成功点击按钮")
							await button.click()
							break

			client.send_read_acknowledge(k)	#将机器人回应设为已读
		
	client.disconnect()
	print("Done! Session name:", session_name[num])		
os._exit(0)
