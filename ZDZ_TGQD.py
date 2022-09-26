import os
import time
import re
import requests
from telethon import TelegramClient, events, sync
from telethon.tl.types import InputMessagesFilterPhotos
proxy = None

api_id = [5672799]	#输入api_id，一个账号一项
api_hash = ['e08529171140eac69071c630f03f1a7a']	#输入api_hash，一个账号一项

robot_map = {'@EmbyPublicBot':'/checkin'}
session_name = api_id[:]

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

#下载验证码图片
def XZYZM():
	photos = client.get_messages(channel_link, None, filter=InputMessagesFilterPhotos)
	index = 0
	for photo in photos:
		filename = channel_link + "/YZM.jpg"
		index = index + 1
		if index == 1:
			client.download_media(photo, filename)
		break
	print("下载完毕")

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
	

for num in range(len(api_id)):
	session_name[num] = "id_" + str(session_name[num])
	client = TelegramClient(session_name[num], api_id[num], api_hash[num])
	client.start()
	
	for (k,v) in robot_map.items():

		client.send_message(k, '/create') #设置机器人和签到命令
		time.sleep(3)
		@client.on(events.NewMessage(chats=k))
		async def handler(event):
			if "帐号剩余有效期:" in event.message.text:
				#print("获取的信息: ", event.message.text)
				print("检查到期天数")
				text = event.message.text.split('帐号剩余有效期:')[1]
				print("text=",text)
				text1 =  text.split('**')[1]
				text1 = re.sub("\D","",text1) 
				print("text1=",text1)
				day = int(text1)
				print("剩余天数=",day)
				if day < 60:
					GetWXMeg('终点站帐号剩余' + str(day) + '天')

		print("执行指令",v)
		client.send_message(k, v) #设置机器人和签到命令
		time.sleep(3)
		@client.on(events.NewMessage(chats=k))
		async def handler(event):
			print("当前签到机器人:", k)
			# 获取带按钮的消息
			print("获取的信息: ", event.message.text)
			if "您距离下次可签到时间还剩" in event.message.text or "已经签到过了" in event.message.text or "/create" in v:
				print("已经签到过了")
			elif "签到验证码" in event.message.text:
				XZYZM()
				time.sleep(3)
				YZM = captcha_solver(channel_link + "/YZM.jpg")
				print("识别的验证码=",YZM)
				#client.send_message(channel_link, YZM) #发送签到验证码
		client.send_read_acknowledge(k)	#将机器人回应设为已读
		client.disconnect()
	print("Done! Session name:", session_name[num])		
os._exit(0)
