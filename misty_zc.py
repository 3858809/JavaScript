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
channel_link = "EmbyMistyBot"
QDmeg = "⚡️注册账号"

TCapikey={
	"sheriqiang@gmail.com":"L7GYXVaB2BreQrGhzh3I",
	"s3858809":"dPwkV7LPndiZmn2rHp81",
	"shexiaoyu":"cLiDO6dflOthLre2fqKb",
	"linyinfei":"ZKWyX71qkCZu25e7AfNO",
	"linchunmiao":"NBX1A27nDnD0NcqlR3fq",
	"xiaochunmiaoyaya2":"jG6O4aUjeaSxrgL07J18",
	"xishi":"7dDVX4Lgl8adm9aQxHEU"
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
		'summary':'Misty注册成功',
		'contentType':1,
		'uids':['UID_8krNXTxaevo6ogJ1g1W3wTnhZpZR'],
		'url':'https%3A%2F%2Fpornemby.club%2Fweb%2Findex.html'
	}
	response = requests.post(url = url, json = data)
	data = response.json()
	return 'ok'

#下载验证码图片
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
		return message.text

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


client.send_message(channel_link, QDmeg) #发送签到命令
i=0
while i < 5 :
	newmeg = HQXX()
	print("获取的新信息=",newmeg)
	if '用户已满' in newmeg or '验证码错误' in newmeg:
		#client.send_message(channel_link,"/cancel")
		time.sleep(1)
		i = i+1
		if i< 5:
			client.send_message(channel_link, QDmeg) #发送签到命令
	elif "输入验证" in  newmeg:
		try:
			XZYZM()#下载验证码图片
			YZM = captcha_solver(channel_link + "/YZM.jpg")
			print("发送验证码=",YZM) 
			client.send_message(channel_link, YZM) #发送签到验证码
			time.sleep(1)
		except:
			client.send_message(channel_link,"/cancel")
		else:
			print("没有异常")
	elif '注册账号' in newmeg:
		print("等待接收图片。。")
	else:
		print("注册成功")
		time.sleep(1)
		GetWXMeg(newmeg)

client.send_read_acknowledge(channel_link) #将机器人回应设为已读
client.disconnect()
print("脚本结束")
