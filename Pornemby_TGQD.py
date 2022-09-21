import os
import time
import json
import requests
from telethon import TelegramClient, events, sync

api_id = [5672799]	#输入api_id，一个账号一项
api_hash = ['e08529171140eac69071c630f03f1a7a']	#输入api_hash，一个账号一项

robot_map = {'@PronembyTGBot2_bot':'/start'}
session_name = api_id[:]

def GetWXMeg(text):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	data = { 
		'appToken':'AT_OdRi5Z4hzWMr225NfPVHhXVSmfN59GeR', 
		'content':text,  
		'summary':'PornEmby自动查看异常',
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
		while i<1:
			i += 1
			client.send_message(k, v) #设置机器人和签到命令
			time.sleep(3)
			@client.on(events.NewMessage(chats=k))
			async def handler(event):
				global i
				print("当前获取对象:", k)
				print("本次为第", i,"次获取信息")
				# 获取带按钮的消息
				print("获取的信息: ", event.message.text)
				if '未使用1天后' in event.message.text or '未使用2天后' in event.message.text or '未使用3天后' in event.message.text or '未使用4天后' in event.message.text or '未使用5天后' in event.message.text or '未使用6天后' in event.message.text or '未使用7天后' in event.message.text or '未使用8天后' in event.message.text:
					GetWXMeg(event.message.text)
				if "您距离下次可签到时间还剩" in event.message.text or "已经签到过了" in event.message.text:
					print("已经签到过了")
					i += 100
				elif event.message.buttons:
					print("发现按钮信息")
					# 匹配按钮文本并点击
					for button in event.message.buttons[0]:
						if '签到' in button.text:
							print("匹配按钮文本成功点击按钮")
							await button.click()
							break

			client.send_read_acknowledge(k)	#将机器人回应设为已读
		
	client.disconnect()
	print("Done! Session name:", session_name[num])		
os._exit(0)
