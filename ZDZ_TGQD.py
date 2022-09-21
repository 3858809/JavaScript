import os
import time
from telethon import TelegramClient, events, sync

api_id = [5672799]	#输入api_id，一个账号一项
api_hash = ['e08529171140eac69071c630f03f1a7a']	#输入api_hash，一个账号一项

robot_map = {'@EmbyPublicBot':'/create','@EmbyPublicBot':'/checkin'}
session_name = api_id[:]
print("开始签到")


def GetWXMeg(text):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	data = { 
		'appToken':'AT_OdRi5Z4hzWMr225NfPVHhXVSmfN59GeR', 
		'content':text,  
		'summary':'终点站帐号到期提醒',
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
	
	for (k,v) in robot_map.items():
		client.send_message(k, v) #设置机器人和签到命令
		time.sleep(3)
		@client.on(events.NewMessage(chats=k))
		async def handler(event):
			print("当前签到机器人:", k)
			# 获取带按钮的消息
			print("获取的信息: ", event.message.text)
			if "您距离下次可签到时间还剩" in event.message.text or "已经签到过了" in event.message.text or "/create" in v:
				print("已经签到过了")
				if "/create" in v:
					text = event.message.text.split('帐号剩余有效期: ')[1]
					day = int(text.split(' 天')[0])
					if day < 200:
						GetWXMeg('终点站帐号剩余' + str(day) + '天')
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

		client.send_read_acknowledge(k)	#将机器人回应设为已读
		client.disconnect()
	print("Done! Session name:", session_name[num])		
os._exit(0)
