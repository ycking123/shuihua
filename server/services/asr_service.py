import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
import asyncio
import websockets
import ssl

class XunfeiASRService:
    def __init__(self, app_id, api_key, api_secret):
        self.app_id = str(app_id).strip()
        self.api_key = str(api_key).strip()
        self.api_secret = str(api_secret).strip()
        self.host = "iat.xf-yun.com"
        self.url = f"wss://{self.host}/v1"
        
        # Match demo parameters exactly
        self.iat_params = {
            "domain": "slm", 
            "language": "zh_cn", 
            "accent": "mandarin",
            "dwa": "wpgs",
            "result": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain"
            }
        }

    def create_url(self):
        """生成鉴权 URL"""
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接签名字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET /v1 HTTP/1.1"

        # hmac-sha256 加密
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 组合成最终的url
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        return self.url + '?' + urllib.parse.urlencode(v)

    async def stream_audio(self, audio_generator, callback):
        """
        连接讯飞 WebSocket 并流式发送音频
        """
        url = self.create_url()
        print(f"Connecting to Xunfei IAT: {url[:60]}...", flush=True)
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        try:
            async with websockets.connect(url, ssl=ssl_context) as ws:
                print("Connected to Xunfei IAT", flush=True)
                
                # 接收任务
                async def receive_msg():
                    try:
                        async for msg in ws:
                            msg_json = json.loads(msg)
                            code = msg_json["header"]["code"]
                            
                            if code != 0:
                                print(f"ASR Error: {code}, {msg_json['header'].get('message')}", flush=True)
                                await callback({"error": f"ASR Error {code}"})
                                # Don't break immediately, let the server close or handle it
                                # But usually code != 0 means fatal error for this session
                                return 
                            
                            payload = msg_json.get("payload")
                            if payload:
                                result = payload.get("result")
                                if result:
                                    text_base64 = result.get("text")
                                    text_json = base64.b64decode(text_base64).decode('utf-8')
                                    data = json.loads(text_json)
                                    res = ""
                                    for w in data['ws']:
                                        for cw in w['cw']:
                                            res += cw['w']
                                    
                                    # Send partial/final result
                                    # ls (last status): boolean, true if last result
                                    is_last = data.get('ls', False)
                                    await callback({"text": res, "is_final": is_last})
                            
                            if msg_json["header"]["status"] == 2:
                                break
                    except Exception as e:
                        print(f"Receive error: {e}", flush=True)

                receive_task = asyncio.create_task(receive_msg())

                # 发送任务
                status = 0 # 0:第一帧, 1:中间帧, 2:最后一帧
                try:
                    async for chunk in audio_generator:
                        if chunk is None:
                            break
                        
                        audio_b64 = str(base64.b64encode(chunk), 'utf-8')
                        
                        # Construct frame data EXACTLY as in the demo
                        # Note: Demo sends 'parameter' in EVERY frame
                        data = {
                            "header": {
                                "status": status,
                                "app_id": self.app_id
                            },
                            "parameter": {
                                "iat": self.iat_params
                            },
                            "payload": {
                                "audio": {
                                    "audio": audio_b64,
                                    "sample_rate": 16000,
                                    "encoding": "raw"
                                }
                            }
                        }
                        
                        if status == 0:
                            print(f"ASR Sending First Frame", flush=True)
                            status = 1 # Next frames are continue frames
                        
                        await ws.send(json.dumps(data))
                        
                        # Use 0.04s interval to match iFlytek recommended rate (40ms)
                        await asyncio.sleep(0.04)

                    # 发送最后一帧 (End of Stream)
                    # Even for last frame, demo sends parameters
                    data = {
                        "header": {
                            "status": 2,
                            "app_id": self.app_id
                        },
                        "parameter": {
                            "iat": self.iat_params
                        },
                        "payload": {
                            "audio": {
                                "audio": "", # Empty audio for last frame
                                "sample_rate": 16000,
                                "encoding": "raw"
                            }
                        }
                    }
                    print("Sent last frame (status 2)", flush=True)
                    await ws.send(json.dumps(data))

                except Exception as e:
                    print(f"Send error: {e}", flush=True)
                
                # Wait for receiver to finish
                await receive_task
                
        except Exception as e:
            print(f"ASR Connection error: {e}", flush=True)
            await callback({"error": str(e)})

