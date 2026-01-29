import os
import logging
from flask import Flask, request, abort, make_response
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.enterprise import parse_message, create_reply
from wechatpy.enterprise.events import SubscribeEvent, UnsubscribeEvent, ClickEvent, ViewEvent, LocationEvent, BatchJobResultEvent
from wechatpy.enterprise.messages import TextMessage, ImageMessage, VoiceMessage, VideoMessage, LocationMessage, LinkMessage
from dotenv import load_dotenv
from pathlib import Path

# --- 异常处理兼容性修正 ---
try:
    from wechatpy.exceptions import InvalidSignatureException, InvalidCorpIdException
except ImportError:
    # wechatpy 1.8.18 可能使用 InvalidAppIdException 代替 InvalidCorpIdException
    from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException as InvalidCorpIdException


# --- 配置日志 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- 加载配置 ---
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("WECOM_TOKEN")
EncodingAESKey = os.getenv("WECOM_AES_KEY")
CORP_ID = os.getenv("WECOM_CORP_ID")

if not all([TOKEN, EncodingAESKey, CORP_ID]):
    logger.error("❌ 缺少必要的企业微信配置 (WECOM_TOKEN, WECOM_AES_KEY, WECOM_CORP_ID)，请检查 .env 文件")
    exit(1)

# 初始化加解密组件
try:
    crypto = WeChatCrypto(TOKEN, EncodingAESKey, CORP_ID)
except Exception as e:
    logger.error(f"❌ 初始化 WeChatCrypto 失败: {e}")
    exit(1)

app = Flask(__name__)

# --- 消息处理器 ---
def handle_message(msg):
    """根据消息类型分发处理逻辑"""
    msg_type = msg.type
    
    # 1. 普通消息处理
    if msg_type == 'text':
        logger.info(f"收到文本消息: {msg.content}")
        # 示例：回复收到的内容
        return create_reply(f"收到您的消息：{msg.content}", msg)
    
    elif msg_type == 'image':
        logger.info(f"收到图片消息，MediaId: {msg.media_id}")
        return create_reply("已收到图片", msg)
        
    elif msg_type == 'voice':
        logger.info(f"收到语音消息，MediaId: {msg.media_id}")
        return create_reply("已收到语音", msg)
        
    elif msg_type == 'video':
        logger.info(f"收到视频消息，MediaId: {msg.media_id}")
        return create_reply("已收到视频", msg)
        
    elif msg_type == 'location':
        logger.info(f"收到位置消息: ({msg.location_x}, {msg.location_y}) - {msg.label}")
        return create_reply("已收到位置信息", msg)
        
    elif msg_type == 'link':
        logger.info(f"收到链接消息: {msg.title} - {msg.url}")
        return create_reply("已收到链接", msg)

    # 2. 事件消息处理
    elif msg_type == 'event':
        event_type = msg.event
        logger.info(f"收到事件推送: {event_type}")
        
        if event_type == 'subscribe':
            return create_reply("欢迎关注！", msg)
        elif event_type == 'unsubscribe':
            logger.info("用户取消关注")
        elif event_type == 'enter_agent':
            logger.info("用户进入应用")
            # return create_reply("欢迎回来！", msg) 
        elif event_type == 'click':
            logger.info(f"菜单点击: {msg.key}")
            return create_reply(f"点击了菜单: {msg.key}", msg)
        elif event_type == 'view':
            logger.info(f"菜单跳转: {msg.url}")
        elif event_type == 'location':
            logger.info(f"上报地理位置: ({msg.latitude}, {msg.longitude})")
        elif event_type == 'batch_job_result':
            logger.info(f"异步任务完成: {msg.job_id}")
        else:
            logger.warning(f"未处理的事件类型: {event_type}")
            
    else:
        logger.warning(f"未知消息类型: {msg_type}")
        
    # 默认回复 success (不回复任何内容给用户，且告诉企微处理成功)
    return "success"


@app.route('/wecom/callback', methods=['GET', 'POST'])
def wechat_callback():
    # 获取通用参数
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    
    if not all([msg_signature, timestamp, nonce]):
        abort(400, "Missing required parameters")

    # --- GET 请求：URL 验证 ---
    if request.method == 'GET':
        echostr = request.args.get('echostr', '')
        logger.info(f"收到 GET 验证请求: signature={msg_signature}, timestamp={timestamp}, nonce={nonce}")
        
        try:
            echostr = crypto.check_signature(msg_signature, timestamp, nonce, echostr)
            if isinstance(echostr, bytes):
                echostr = echostr.decode('utf-8')
            logger.info("✅ URL 验证成功")
            return make_response(echostr)
        except InvalidSignatureException:
            logger.error("❌ 签名验证失败")
            abort(403)
        except Exception as e:
            logger.error(f"❌ URL 验证异常: {e}")
            abort(500)

    # --- POST 请求：消息接收 ---
    if request.method == 'POST':
        try:
            # 获取原始 XML 数据
            xml_data = request.get_data()
            logger.info(f"收到 POST 请求，数据长度: {len(xml_data)}")
            
            # 1. 解密消息
            decrypted_xml = crypto.decrypt_message(
                xml_data,
                msg_signature,
                timestamp,
                nonce
            )
            logger.debug(f"解密后的 XML: {decrypted_xml}")
            
            # 2. 解析消息
            msg = parse_message(decrypted_xml)
            logger.info(f"解析消息成功: type={msg.type}, from={msg.source}")
            
            # 3. 业务逻辑处理
            reply = handle_message(msg)
            
            # 4. 构造响应
            if reply == "success":
                return "success"
            
            # 如果是 Reply 对象，需要渲染成 XML 并加密
            xml_response = reply.render()
            encrypted_response = crypto.encrypt_message(xml_response, nonce, timestamp)
            
            response = make_response(encrypted_response)
            response.headers['Content-Type'] = 'application/xml'
            return response

        except InvalidSignatureException:
            logger.error("❌ 消息签名验证失败")
            abort(403)
        except InvalidCorpIdException:
            logger.error("❌ CorpID 不匹配")
            abort(403)
        except Exception as e:
            logger.error(f"❌ 消息处理异常: {e}")
            # 即使出错也返回 success，避免企微无限重试
            return "success"

if __name__ == '__main__':
    # 监听 8080 端口 (避免 80 端口权限问题)
    port = 8080
    logger.info(f"🚀 企业微信消息接收服务已启动，监听端口: {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
