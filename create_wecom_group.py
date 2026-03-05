import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from wechatpy.enterprise import WeChatClient

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CreateGroup")

# Load Environment Variables
# Try loading from backend/.env
env_path = Path(__file__).parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

# Try loading from root .env.local
root_env_path = Path(__file__).parent / ".env.local"
load_dotenv(dotenv_path=root_env_path)

WECOM_CORP_ID = os.getenv("WECOM_CORP_ID")
WECOM_SECRET = os.getenv("WECOM_SECRET")

def create_wecom_group(user_ids, chat_name="水华精灵测试群", owner=None):
    """
    创建企业微信群聊
    :param user_ids: 群成员 UserID 列表 (list)
    :param chat_name: 群聊名称
    :param owner: 群主 UserID (可选)
    :return: chatid (str) or None
    """
    if not all([WECOM_CORP_ID, WECOM_SECRET]):
        logger.error("❌ 缺少 WECOM_CORP_ID 或 WECOM_SECRET 环境变量")
        return None

    try:
        client = WeChatClient(WECOM_CORP_ID, WECOM_SECRET)
        
        logger.info(f"🚀 正在创建群聊: {chat_name}")
        logger.info(f"👥 成员列表: {user_ids}")
        
        # appchat.create(chat_id=None, name=None, owner=None, user_list=None)
        # Note: user_list is required. owner is optional.
        res = client.appchat.create(name=chat_name, owner=owner, user_list=user_ids)
        
        chatid = res.get("chatid")
        logger.info(f"✅ 群聊创建成功! ChatID: {chatid}")
        
        # Send a welcome message
        client.appchat.send_text(chatid, "大家好，我是水华精灵！本群聊已创建成功。")
        logger.info("📨 已发送欢迎消息")
        
        return chatid
        
    except Exception as e:
        logger.error(f"❌ 创建群聊失败: {e}")
        return None

if __name__ == "__main__":
    # 指定要加入群聊的用户 ID
    # 注意：企业微信接口要求群成员至少 2 人，或者可能允许 1 人 + 机器人？
    # 如果只填 1 个用户报错，请尝试添加更多用户 ID
    target_users = ["lanjing", "ZhangXiaoYan"] 
    
    # 运行函数
    create_wecom_group(target_users, chat_name="水华精灵-交流群")
