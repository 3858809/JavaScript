import os
import time
from telethon import TelegramClient, events, sync

api_id = [5672799]	#输入api_id，一个账号一项
api_hash = ['e08529171140eac69071c630f03f1a7a']	#输入api_hash，一个账号一项

robot_map = {'@qweybgbot':'/checkin'}
session_name = api_id[:]
print("开始签到")

def fujs(fuhao,formstr):
	print("开始计算")
	jg = 0
	if "加" == fuhao or "+" == fuhao or "加以" == fuhao or "枷" == fuhao:
		jg = int(formstr.split(' ')[0]) + int(formstr.split(' ')[2])
	elif "减" == fuhao or "-" == fuhao or "缄" == fuhao or "椷" == fuhao:
		jg = int(formstr.split(' ')[0]) - int(formstr.split(' ')[2])
	elif "乘" == fuhao or "*" == fuhao or "乗以" == fuhao or "騬以" == fuhao or "×" == fuhao:
		jg = int(formstr.split(' ')[0]) * int(formstr.split(' ')[2])
	elif "除" == fuhao or "/" == fuhao or "除以" == fuhao or "處以" == fuhao or "chu以" == fuhao:
		jg = int(formstr.split(' ')[0]) / int(formstr.split(' ')[2])
	else:
		print("没有匹配到计算符号")
		jg = 10086
		
	print("计算结果=",jg)
	return jg

for num in range(len(api_id)):
	session_name[num] = "id_" + str(session_name[num])
	client = TelegramClient(session_name[num], api_id[num], api_hash[num])
	client.start()
	
	for (k,v) in robot_map.items():
		i = 0
		while i<10:
			i += 1
			client.send_message(k, v) #设置机器人和签到命令
			time.sleep(3)
			@client.on(events.NewMessage(chats=k))
			async def handler(event):
				global i
				print("当前签到机器人:", k)
				print("本次为第", i,"次签到")
				# 获取带按钮的消息
				print("获取的信息: ", event.message.text)
				if "您距离下次可签到时间还剩" in event.message.text or "已经签到过了" in event.message.text:
					print("已经签到过了")
					i += 100
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
					result = fujs(js,formula)
					print("计算结果:", result)
					if result != 10086 :
						i += 100
						
					# 匹配按钮文本并点击
					for button in event.message.buttons[0]:
						if int(button.text) == result:
							await button.click()
							break

			client.send_read_acknowledge(k)	#将机器人回应设为已读
		
	client.disconnect()
	print("Done! Session name:", session_name[num])		
os._exit(0)
