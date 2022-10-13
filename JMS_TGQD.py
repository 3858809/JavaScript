import os
import time
import asyncio
import base64
import json
import re
import requests

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
channel_link = "qweybgbot"
QDmeg = "/checkin"
#proxy =("socks5","localhost",12345) #不需要代理的话删掉该行
# ==========================================
client = TelegramClient('shexiaoyu',api_id=api_id,api_hash=api_hash,proxy=proxy).start()

API_KEY = '*********' # 自行获取
SECRET_KEY = '************'  # 自行获取
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"  # OCR接口
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'  # TOKEN获取接口

def fetch_token():
    # 获取token
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    try:
        f = requests.post(TOKEN_URL, params, timeout=5)
        if f.status_code == 200:
            result = f.json()
            if 'access_token' in result.keys() and 'scope' in result.keys():
                if not 'brain_all_scope' in result['scope'].split(' '):
                    return None, 'please ensure has check the  ability'
                return result['access_token'], ''
            else:
                return None, '请输入正确的 API_KEY 和 SECRET_KEY'
        else:
            return None, '请求token失败: code {}'.format(f.status_code)
    except BaseException as err:
        return None, '请求token失败: {}'.format(err)

def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')  # 二进制读取图片信息
        return f.read(), ''
    except BaseException as e:
        return None, '文件({0})读取失败: {1}'.format(image_path, e)
    finally:
        if f:
            f.close()

def pic2text(img_path):
    def request_orc(img_base, token):
        """
        调用百度OCR接口，图片识别文字
        :param img_base: 图片的base64转码后的字符
        :param token: fetch_token返回的token
        :return: 返回一个识别后的文本字典
        """
        try:
            req = requests.post(
                OCR_URL + "?access_token=" + token,
                data={'image': img_base},
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            if req.status_code == 200:
                result = req.json()
                if 'words_result' in result.keys():
                    return req.json()["words_result"], ''
                elif 'error_msg' in result.keys():
                    return None, '图片识别失败: {}'.format(req.json()["error_msg"])

            else:
                return None, '图片识别失败: code {}'.format(req.status_code)
        except BaseException as err:
            return None, '图片识别失败: {}'.format(err)

    file_content, file_error = read_file(img_path)
    if file_content:
        token, token_err = fetch_token()
        if token:
            results, result_err = request_orc(base64.b64encode(file_content), token)
            if result_err: # 打印失败信息
                print(result_err)
            for result in results: # 打印处理结果
                print(result)


#微信提醒
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

def HQXX():
	for message in client.iter_messages(channel_link):
		return message

		
#识别图片验证码
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
	
client.send_message(channel_link, QDmeg) #发送签到命令
while 1==1:
	time.sleep(2)
	newmeg = HQXX()
	print("获取的新信息=",newmeg.text)
	if newmeg.text == '/checkin':
		client.send_message(channel_link,"/cancel")
		time.sleep(1)
		client.send_message(channel_link, QDmeg) #发送签到命令
	elif "请按顺序点击图片中出现的文字" in  newmeg.text:
		XZYZM()#下载验证码图片
		##YZM = captcha_solver(channel_link + "/YZM.jpg")
		YZM = pic2text(channel_link + "/YZM.jpg")
		print("发送验证码=",YZM) 
		
		for j in YZM:
			print j
			for button in newmeg.buttons[0]:
				if j in button.text:
					print("匹配按钮文本成功点击按钮:"+j)
					await button.click()
					break
		
		#client.send_message(channel_link, YZM) #发送签到验证码
		time.sleep(3)
	elif "已经签到过了" in newmeg.text or "签到成功" in newmeg.text:
		print("已经签到过")
		#已经签到过 查询到期时间
		print("开始查询到期时间")
		client.send_message(channel_link, "/create") #发送签到验证码
		time.sleep(1)
		newmeg = HQXX()
		text = newmeg.text.split('帐号剩余有效期:')[1]
		print("text=",text)
		text1 =  text.split('**')[1]
		text1 = re.sub("\D","",text1) 
		print("text1=",text1)
		day = int(text1)
		print("剩余天数=",day)
		if day < 60:
			GetWXMeg('终点站帐号剩余' + str(day) + '天')
		break
	else:
		client.send_message(channel_link, QDmeg) #发送签到验证码

client.send_read_acknowledge(channel_link) #将机器人回应设为已读
client.disconnect()
print("脚本结束")
