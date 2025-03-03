from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import asyncio
import logging
import configparser
from PIL import Image
import pytesseract
import io
import requests
import re
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取全局配置
API_ID = config.get('Telegram', 'API_ID')
API_HASH = config.get('Telegram', 'API_HASH')
PHONE_NUMBER = config.get('Telegram', 'PHONE_NUMBER')
PUSHDEER_KEY = config.get('PushDeer', 'PUSHDEER_KEY')  # PushDeer 的 PushKey

# 初始化 Telegram 客户端
client = TelegramClient('session_name', API_ID, API_HASH)

async def solve_captcha(image_data):
    """
    识别图片验证码
    :param image_data: 图片的二进制数据
    :return: 识别到的验证码文本
    """
    try:
        # 将图片数据转换为 PIL 图像
        image = Image.open(io.BytesIO(image_data))
        # 使用 Tesseract OCR 识别验证码
        captcha_text = pytesseract.image_to_string(image, config='--psm 8')
        logger.info(f"识别到的验证码: {captcha_text}")
        return captcha_text.strip()
    except Exception as e:
        logger.error(f"验证码识别失败: {e}")
        return None

async def send_pushdeer_notification(title, message):
    """
    通过 PushDeer 发送通知
    :param title: 通知标题
    :param message: 通知内容
    """
    try:
        url = "https://api2.pushdeer.com/message/push"
        payload = {
            "pushkey": PUSHDEER_KEY,
            "text": title,
            "desp": message,
            "type": "markdown"
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logger.info("PushDeer 通知发送成功！")
        else:
            logger.error(f"PushDeer 通知发送失败: {response.text}")
    except Exception as e:
        logger.error(f"PushDeer 通知发送异常: {e}")

def parse_expiry_date(message_text):
    """
    从消息文本中解析过期时间
    :param message_text: 机器人的回复消息文本
    :return: 过期时间（datetime 对象），如果未找到则返回 None
    """
    try:
        # 使用正则表达式匹配日期（格式：YYYY-MM-DD 或 YYYY年MM月DD日）
        date_pattern = r"(\d{4}-\d{2}-\d{2})|(\d{4}年\d{2}月\d{2}日)"
        match = re.search(date_pattern, message_text)
        if match:
            date_str = match.group(0)
            # 统一转换为 YYYY-MM-DD 格式
            if "年" in date_str:
                date_str = date_str.replace("年", "-").replace("月", "-").replace("日", "")
            return datetime.strptime(date_str, "%Y-%m-%d")
        return None
    except Exception as e:
        logger.error(f"解析过期时间失败: {e}")
        return None

async def handle_bot_message(event, bot_rules):
    """
    处理机器人回复消息
    :param event: 机器人回复消息事件
    :param bot_rules: 当前机器人的规则列表
    """
    message_text = event.message.message
    logger.info(f"收到消息: {message_text}")

    # 遍历机器人的规则
    for rule in bot_rules:
        pattern = rule.get('pattern')
        action = rule.get('action')
        response = rule.get('response', '')
        notify_days = rule.get('notify_days', None)  # 获取提醒天数配置

        # 检查是否匹配规则
        if re.search(pattern, message_text, re.IGNORECASE):
            logger.info(f"匹配到规则: {pattern} -> {action}")

            if action == "click_button":
                # 点击按钮
                if event.message.reply_markup:
                    for row in event.message.reply_markup.rows:
                        for button in row.buttons:
                            if re.search(response, button.text, re.IGNORECASE):
                                await client(GetBotCallbackAnswerRequest(
                                    peer=event.message.peer_id,
                                    msg_id=event.message.id,
                                    data=button.data
                                ))
                                logger.info(f"已点击按钮: {button.text}")
                                return

            elif action == "send_message":
                # 发送消息
                await client(SendMessageRequest(
                    peer=await event.get_input_chat(),
                    message=response
                ))
                logger.info(f"已发送消息: {response}")

            elif action == "send_notification":
                # 发送 PushDeer 通知
                await send_pushdeer_notification("签到提醒", message_text)
                logger.info(f"已发送 PushDeer 通知: {message_text}")

            elif action == "check_expiry":
                # 检查过期时间并发送提醒
                expiry_date = parse_expiry_date(message_text)
                if expiry_date:
                    remaining_days = (expiry_date - datetime.now()).days
                    if remaining_days <= int(notify_days):
                        await send_pushdeer_notification(
                            "过期提醒",
                            f"您的服务将在 {remaining_days} 天后过期，过期时间：{expiry_date.strftime('%Y-%m-%d')}"
                        )
                        logger.info(f"已发送过期提醒: 剩余 {remaining_days} 天")

async def sign_in_for_bot(bot_username, bot_rules):
    """
    为指定机器人执行签到
    :param bot_username: 机器人的用户名
    :param bot_rules: 当前机器人的规则列表
    """
    try:
        # 查找签到机器人
        bot_entity = await client.get_entity(bot_username)

        # 发送初始签到命令
        await client(SendMessageRequest(
            peer=bot_entity,
            message="/start"  # 初始命令
        ))
        logger.info(f"已向 {bot_username} 发送初始命令")

        # 监听机器人的回复
        @client.on(events.NewMessage(from_users=bot_entity))
        async def handle_message(event):
            await handle_bot_message(event, bot_rules)

        # 等待机器人回复
        await asyncio.sleep(10)  # 根据需要调整等待时间

    except Exception as e:
        logger.error(f"{bot_username} 签到失败: {e}")
        await send_pushdeer_notification("签到失败", f"{bot_username} 签到失败: {e}")

async def auto_sign_in():
    """
    主函数：自动签到
    """
    try:
        # 连接 Telegram
        await client.connect()
        if not await client.is_user_authorized():
            # 发送登录验证码
            await client.send_code_request(PHONE_NUMBER)
            code = input("请输入收到的验证码: ")
            await client.sign_in(PHONE_NUMBER, code)

        logger.info("登录成功！")

        # 遍历所有签到机器人配置
        for section in config.sections():
            if section.startswith("Bot_"):
                bot_username = config.get(section, 'BOT_USERNAME')
                bot_rules = []

                # 加载机器人的规则
                for key, value in config.items(section):
                    if key.startswith("rule_"):
                        rule = {
                            'pattern': config.get(section, f"{key}_pattern"),
                            'action': config.get(section, f"{key}_action"),
                            'response': config.get(section, f"{key}_response", fallback=""),
                            'notify_days': config.get(section, f"{key}_notify_days", fallback=None)
                        }
                        bot_rules.append(rule)

                await sign_in_for_bot(bot_username, bot_rules)

    except Exception as e:
        logger.error(f"签到失败: {e}")
        await send_pushdeer_notification("签到失败", f"签到失败: {e}")
    finally:
        await client.disconnect()

# 运行脚本
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(auto_sign_in())
