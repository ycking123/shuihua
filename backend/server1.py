# from flask import Flask, request, abort
# from wechatpy.enterprise.crypto import WeChatCrypto
# from wechatpy.exceptions import InvalidSignatureException
# from wechatpy.enterprise import parse_message

# app = Flask(__name__)

# # ============================================================
# # 请再次确认这三项（不要有空格！）
# # ============================================================
# TOKEN = 'tgUsidLKMFkw7wVjkMohc8a'
# EncodingAESKey = 'vmPawblaBX2QhirIEDhsJhlNCT397SCPOlUqVyelLLn'
# CORP_ID = 'wwcd40432aceae49af'

# crypto = WeChatCrypto(TOKEN, EncodingAESKey, CORP_ID)

# @app.route('/wecom/callback', methods=['GET', 'POST'])
# def wechat_callback():
#     # 打印所有参数，看看企微到底传了什么过来
#     print(f"\n======== 收到新请求 {request.method} ========")
#     msg_signature = request.args.get('msg_signature', '')
#     timestamp = request.args.get('timestamp', '')
#     nonce = request.args.get('nonce', '')
#     echostr = request.args.get('echostr', '')
    
#     print(f"1. 接收到的签名 (signature): {msg_signature}")
#     print(f"2. 接收到的时间戳 (timestamp): {timestamp}")
#     print(f"3. 接收到的随机数 (nonce):     {nonce}")

#     if request.method == 'GET':
#         try:
#             # 这里的 check_signature 会自动计算正确的签名并对比
#             print("4. 正在尝试验证签名...")
#             decrypted_echostr = crypto.check_signature(
#                 msg_signature,
#                 timestamp,
#                 nonce,
#                 echostr
#             )
#             print("✅ 验证成功！解密后的 echostr:", decrypted_echostr)
#             return decrypted_echostr
            
#         except InvalidSignatureException:
#             # 【关键】这里会告诉你为什么失败
#             print("❌ 验证失败！签名不匹配。")
#             print("   -> 可能原因：企微发送的请求是用旧Token加密的，或者代码里的Token填错了。")
#             abort(403)
#         except Exception as e:
#             print(f"❌ 发生其他错误: {e}")
#             abort(403)

#     if request.method == 'POST':
#         # (POST逻辑省略，调试阶段先通过GET)
#         return "success"

# if __name__ == '__main__':
#     # 强制使用 5000 端口，避开 80 端口的干扰
#     print("🚀 调试服务已启动，监听 80 端口...")
#     app.run(host="0.0.0.0", port=80, debug=True)

from flask import Flask, request, abort, Response
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
import struct
import base64

app = Flask(__name__)

TOKEN = 'tgUsidLKMFkw7wVjkMohc8a'
EncodingAESKey = 'vmPawblaBX2QhirIEDhsJhlNCT397SCPOlUqVyelLLn'
CORP_ID = 'wwcd40432aceae49af'

crypto = WeChatCrypto(TOKEN, EncodingAESKey, CORP_ID)

def extract_msg_from_decrypted(decrypted_bytes):
    """从解密后的字节中提取 msg 字段"""
    if isinstance(decrypted_bytes, str):
        decrypted_bytes = decrypted_bytes.encode('utf-8')
    
    # 结构: random(16B) + msg_len(4B, 大端序) + msg + CorpID
    msg_len = struct.unpack(">I", decrypted_bytes[16:20])[0]
    msg = decrypted_bytes[20:20+msg_len].decode('utf-8')
    return msg

@app.route('/wecom/callback', methods=['GET', 'POST'])
def wechat_callback():
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')

    print(f"\n收到 GET 请求:")
    print(f"  msg_signature: {msg_signature}")
    print(f"  timestamp: {timestamp}")
    print(f"  nonce: {nonce}")
    print(f"  echostr: {echostr[:50]}...")

    if request.method == 'GET':
        try:
            # 验证签名并解密
            decrypted = crypto.check_signature(msg_signature, timestamp, nonce, echostr)
            print(f"  解密后原始数据类型: {type(decrypted)}")
            
            # 如果是 bytes，需要提取 msg；如果是 str（旧版本 wechatpy），直接处理
            if isinstance(decrypted, bytes):
                msg = extract_msg_from_decrypted(decrypted)
            else:
                # 尝试解析，如果不是纯数字，可能需要提取
                msg = str(decrypted)
                # 如果是类似 "4031565423483402943" 这种，就是 msg 本身
                if not msg.isdigit():
                    # 可能是完整结构，尝试提取
                    msg = extract_msg_from_decrypted(msg.encode())
            
            print(f"  提取到的 msg: {msg}")
            
            # 原样返回 msg，确保是纯文本，无引号、无 BOM、无换行
            return Response(msg.strip(), mimetype='text/plain')
            
        except Exception as e:
            print(f"  错误: {e}")
            abort(403)

    return "success"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

# from flask import Flask, request, abort, Response
# from wechatpy.enterprise.crypto import WeChatCrypto
# from wechatpy.exceptions import InvalidSignatureException, InvalidCorpIdException
# import traceback
# import urllib.parse

# app = Flask(__name__)

# ============================================================
# 企业微信配置参数（必须与企业微信后台配置完全一致）
# # ============================================================
# TOKEN = 'your_token_here'  # 从企业微信后台获取的Token
# EncodingAESKey = 'your_encoding_aes_key_here'  # 从企业微信后台获取的EncodingAESKey
# CORP_ID = 'your_corp_id_here'  # 企业微信的CorpID

# from flask import Flask, request, abort, Response
# from wechatpy.enterprise.crypto import WeChatCrypto
# from wechatpy.exceptions import InvalidSignatureException
# from wechatpy.enterprise import parse_message
# import traceback
# # 如果遇到URL编码问题，可以用这个手动解码，但通常Flask会自动处理
# from urllib.parse import unquote 

# app = Flask(__name__)

# # ============================================================
# # 请再次确认这三项
# # ============================================================
# TOKEN = 'tgUsidLKMFkw7wVjkMohc8a'
# EncodingAESKey = 'vmPawblaBX2QhirIEDhsJhlNCT397SCPOlUqVyelLLn'
# CORP_ID = 'wwcd40432aceae49af'

# crypto = WeChatCrypto(TOKEN, EncodingAESKey, CORP_ID)

# @app.route('/wecom/callback', methods=['GET', 'POST'])
# def wechat_callback():
#     # 打印所有参数，方便排查
#     print(f"\n======== 收到新请求 {request.method} ========")
    
#     msg_signature = request.args.get('msg_signature', '')
#     timestamp = request.args.get('timestamp', '')
#     nonce = request.args.get('nonce', '')
#     echostr = request.args.get('echostr', '')

#     print(f"1. 接收到的签名: {msg_signature}")
#     print(f"2. 接收到的时间戳: {timestamp}")
#     print(f"3. 接收到的随机数: {nonce}")
#     print(f"4. 接收到的 echostr: {echostr}")

#     if request.method == 'GET':
#         try:
#             print("5. 正在验证签名并解密...")
            
#             # wechatpy 的 check_signature 会自动完成以下步骤：
#             # 1. 校验签名
#             # 2. AES解密
#             # 3. 去除16位随机字符、去除msg_len、去除CorpID
#             # 4. 返回纯净的 msg 内容 (bytes类型)
#             decrypted_echostr = crypto.check_signature(
#                 msg_signature,
#                 timestamp,
#                 nonce,
#                 echostr
#             )
            
#             # 【重要修改】decrypted_echostr 是 bytes 类型
#             # 千万不要用 str() 强转，否则会变成 "b'xyz'" 导致验证失败
#             # 必须使用 .decode('utf-8') 还原为纯字符串
#             if isinstance(decrypted_echostr, bytes):
#                 decrypted_echostr = decrypted_echostr.decode('utf-8')
                
#             print(f"✅ 验证成功！解密后的纯明文: [{decrypted_echostr}]")

#             # 构造 Response，确保没有引号，没有换行，MIME 类型纯文本
#             return Response(decrypted_echostr, mimetype='text/plain')
            
#         except InvalidSignatureException:
#             print("❌ 验证失败：签名不匹配。")
#             # 只有签名对不上才会抛这个错，通常是 Token 填错或 URL 编码问题
#             abort(403)
#         except Exception as e:
#             print("❌ GET 处理异常：")
#             traceback.print_exc()
#             abort(500)

#     if request.method == 'POST':
#         try:
#             # 获取原始 XML 数据
#             xml_data = request.get_data() # 获取 bytes 原始数据更稳妥
            
#             print("6. 收到 POST 请求")

#             # 解密 XML 消息
#             # wechatpy 同样会自动去掉随机串和CorpID，只返回 xml 文本
#             decrypted_xml = crypto.decrypt_message(
#                 xml_data,
#                 msg_signature,
#                 timestamp,
#                 nonce
#             )
            
#             # 这里如果 decrypted_xml 是 bytes，也要解码
#             if isinstance(decrypted_xml, bytes):
#                  decrypted_xml = decrypted_xml.decode('utf-8')

#             print("✅ POST 消息解密成功，XML内容：\n", decrypted_xml)

#             # 解析 XML 为对象
#             msg = parse_message(decrypted_xml)
#             print("8. 解析后的消息对象：", msg)

#             # --- 业务逻辑处理区域 ---
#             # if msg.type == 'text':
#             #     print("收到文本消息：", msg.content)
#             # ---------------------

#             return "success"
            
#         except InvalidSignatureException as e:
#             print("❌ POST 签名校验失败：", e)
#             abort(403)
#         except Exception:
#             print("❌ POST 处理异常")
#             traceback.print_exc()
#             abort(500)

# if __name__ == '__main__':
#     print("🚀 服务已启动，监听 80 端口...")
#     app.run(host="0.0.0.0", port=80, debug=True)