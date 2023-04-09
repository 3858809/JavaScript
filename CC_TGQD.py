import os
import time
import asyncio
import base64
import json
import re
import requests
import datetime

from telethon import TelegramClient,sync
from telethon.tl.types import InputMessagesFilterPhotos
proxy = None
# =============需要被替换的值=================
'''
api_id 你的api id
api_hash 你的api hash
channel_link 要下载图片的频道链接
proxy 将localhost改成代理地址,12345改成代理端口
picture_storage_path 图片下载到的路径
'''
api_id = 5672799
api_hash = "e08529171140eac69071c630f03f1a7a"
channel_link = "EmbyCc_bot"
QDmeg = "/start"
#图片验证码api字典
TCapikey={
	"123":"123",
	"123":"123"
}

#proxy =("socks5","localhost",12345) #不需要代理的话删掉该行
# ==========================================
client = TelegramClient('shexiaoyu',api_id=api_id,api_hash=api_hash,proxy=proxy).start()

#微信提醒
def GetWXMeg(text):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	data = { 
		'appToken':'AT_OdRi5Z4hzWMr225NfPVHhXVSmfN59GeR', 
		'content':text,  
		'summary':'CC公益服帐号到期提醒',
		'contentType':1,
		'uids':['UID_8krNXTxaevo6ogJ1g1W3wTnhZpZR'],
		'url':'https%3A%2F%2Fpornemby.club%2Fweb%2Findex.html'
	}
	response = requests.post(url = url, json = data)
	data = response.json()
	return 'ok'

def XZYZM():
	print("开始获取频道photos")
	#photos = client.get_messages(channel_link, None, filter=InputMessagesFilterPhotos)
	print("获取完毕")
	index = 0
	for photo in client.iter_messages(channel_link, None, filter=InputMessagesFilterPhotos):
	#for photo in photos:
		filename = channel_link + "/YZM.jpg"
		index = index + 1
		if index == 1:
			print("开始下载最新的一张图片")
			client.download_media(photo, filename)
			print("下载完毕")
		break
	print("退出下载")

def HQXX():
	for message in client.iter_messages(channel_link):
		return message

def captcha_solver(f):
	for key in TCapikey :
		print("开始进行验证码识别，使用账号：")
		print("userid=",key)
		print("key=",TCapikey[key])
		with open(f, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read()).decode('ascii')
			url = 'https://api.apitruecaptcha.org/one/gettext'
			data = { 
				'userid':key, 
				'apikey':TCapikey[key],  
				'data':encoded_string
			}
			response = requests.post(url = url, json = data)
			data = response.json()
			print("data=",data)
			if "result" in data:
				return data['result']
			else :
				print("账号免费数量用完：",key)
	
	print("全部账号的免费数量都用完了")	
	
def setjson(key,text):
	with open("/home/tgqd/qd.json", "r",encoding='utf-8') as jsonFile:
		data = json.load(jsonFile)
	tmp = data[key]
	data[key] = text
	with open("/home/tgqd/qd.json", "w") as jsonFile:
		json.dump(data, jsonFile,ensure_ascii=False)

def getjson(key):
	with open("/home/tgqd/qd.json", "r",encoding='utf-8') as jsonFile:
		data = json.load(jsonFile)
	return data[key]

qdsj = getjson("cc") 
print("CC公益服上一次签到时间：",qdsj) 
dqsj = str(datetime.date.today())
print("当前时间：",dqsj)

dqsj_t = datetime.datetime.strptime(dqsj, "%Y-%m-%d")
qdsj_t = datetime.datetime.strptime(qdsj, "%Y-%m-%d")
if dqsj_t > qdsj_t:
	client.send_message(channel_link, QDmeg) #发送签到命令
time.sleep(3)
while dqsj_t > qdsj_t:
	time.sleep(30)
	newmeg = HQXX()
	print("获取的新信息=",newmeg.text)
	time.sleep(10)
	if "请在下方选择您要使用的功能" in  newmeg.text:
		print("进入签到操作页面")
		for button in newmeg.buttons[1]:
			print("按钮文本=",button.text)
			if "签到" in button.text:
				button.click()
	elif "请输入验证码" in newmeg.text:
		print("已经进入了验证码阶段")
		XZYZM()#下载验证码图片
		YZM = captcha_solver(channel_link + "/YZM.jpg")
		print("发送验证码=",YZM)
		client.send_message(channel_link, YZM) #发送签到验证码
		time.sleep(10)			
	elif "已经签到" in newmeg.text or "到成功，获得了" in newmeg.text:
		print("已经签到过")
		setjson("cc",str(datetime.date.today()))
		qdsj = getjson("cc")
		qdsj_t = datetime.datetime.strptime(qdsj, "%Y-%m-%d")
	else:
		client.send_message(channel_link, QDmeg) #发送签到验证码
client.send_read_acknowledge(channel_link) #将机器人回应设为已读
client.disconnect()
print("脚本结束")
