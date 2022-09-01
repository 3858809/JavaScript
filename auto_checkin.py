import os
import time
from telethon import TelegramClient, events, sync

api_id = [5672799]	#输入api_id，一个账号一项
api_hash = ['e08529171140eac69071c630f03f1a7a']	#输入api_hash，一个账号一项

robot_map = {'@EmbyPublicBot':'/checkin','@qweybgbot':'/checkin'}

session_name = api_id[:]
for num in range(len(api_id)):
	session_name[num] = "id_" + str(session_name[num])
	client = TelegramClient(session_name[num], api_id[num], api_hash[num])
	client.start()
	for (k,v) in robot_map.items():
		print("Start checkin: ", k)
		client.send_message(k, v) #设置机器人和签到命令
		time.sleep(3)
		@client.on(events.NewMessage(chats=[5672799]))
		async def handler(event):
			# 获取带按钮的消息
			if "已经签到过了" in event.message.text:
				await client.disconnect()
			elif event.message.buttons:
				# 获取算式
				# '签到需要确认问题并选择您认为正确的答案：\n\n25 + 1 = ?\n\n请在 30 秒内作答'
				formula = event.message.raw_text.split('\n\n')[1]
				# 计算结果 25 + 1 = ?
				result = int(formula.split(' ')[0]) + int(formula.split(' ')[2])
				# 匹配按钮文本并点击
				for button in event.message.buttons[0]:
					if int(button.text) == result:
						await button.click()
						break
				# 结束异步任务
				await client.disconnect()
		client.send_read_acknowledge(k)	#将机器人回应设为已读
	print("Done! Session name:", session_name[num])	
os._exit(0)
