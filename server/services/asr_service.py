import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from datetime import datetime, timezone, timedelta
import asyncio
import websockets
import ssl
import uuid

# 全局配置：与服务端确认的固定参数 (参考 Demo)
FIXED_PARAMS = {
    "audio_encode": "pcm_s16le",
    "lang": "autodialect",
    "samplerate": "16000"
}
# 16k采样率，16bit位深，单声道 => 32KB/s => 32 bytes/ms
# Demo 建议 40ms 发送 1280 bytes
AUDIO_FRAME_SIZE = 1280 
FRAME_INTERVAL_S = 0.04 # 40ms

class XunfeiASRService:
    def __init__(self, app_id, api_key, api_secret):
        self.app_id = app_id
        self.access_key_id = api_key      # API_KEY 对应 accessKeyId
        self.access_key_secret = api_secret # API_SECRET 对应 accessKeySecret
        
        # 使用 Demo 提供的 URL
        self.base_url = "wss://office-api-ast-dx.iflyaisol.com/ast/communicate/v1"

    def _get_utc_time(self):
        """生成服务端要求的UTC时间格式：yyyy-MM-dd'T'HH:mm:ss+0800"""
        beijing_tz = timezone(timedelta(hours=8))
        now = datetime.now(beijing_tz)
        return now.strftime("%Y-%m-%dT%H:%M:%S%z")

    def create_url(self):
        """生成鉴权 URL (参考 Demo _generate_auth_params)"""
        auth_params = {
            "accessKeyId": self.access_key_id,
            "appId": self.app_id,
            "uuid": uuid.uuid4().hex,
            "utc": self._get_utc_time(),
            **FIXED_PARAMS
        }

        # 计算签名：过滤空值 → 字典序排序 → URL编码 → 拼接基础字符串
        sorted_params = dict(sorted([
            (k, v) for k, v in auth_params.items()
            if v is not None and str(v).strip() != ""
        ]))
        
        base_str = "&".join([
            f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}"
            for k, v in sorted_params.items()
        ])

        # HMAC-SHA1 加密 + Base64编码
        signature = hmac.new(
            self.access_key_secret.encode("utf-8"),
            base_str.encode("utf-8"),
            hashlib.sha1
        ).digest()
        
        auth_params["signature"] = base64.b64encode(signature).decode("utf-8")
        
        # 生成完整 URL
        params_str = urllib.parse.urlencode(auth_params)
        return f"{self.base_url}?{params_str}"

    async def stream_audio(self, audio_generator, callback):
        """
        连接讯飞 RTASR WebSocket 并流式发送音频
        """
        url = self.create_url()
        print(f"Connecting to Xunfei RTASR: {url[:60]}...", flush=True)
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        try:
            async with websockets.connect(url, ssl=ssl_context, ping_interval=20, ping_timeout=20) as ws:
                print("Connected to Xunfei RTASR", flush=True)
                
                # 接收任务
                async def receive_msg():
                    try:
                        while True:
                            try:
                                msg = await ws.recv()
                            except websockets.exceptions.ConnectionClosed:
                                print("ASR WebSocket connection closed by remote", flush=True)
                                break
                                
                            msg_json = json.loads(msg)
                            
                            action = msg_json.get("action")
                            msg_type = msg_json.get("msg_type")
                            code = msg_json.get("code")
                            
                            if code and code != "0":
                                print(f"ASR Error Code: {code}, Msg: {msg_json}", flush=True)

                            if msg_type == "result" or action == "result":
                                data = msg_json.get("data")
                                if data:
                                    try:
                                        # 如果 data 是字符串，则解析；如果是字典，直接使用
                                        if isinstance(data, str):
                                            data = json.loads(data)
                                        
                                        # 解析 RTASR 结果结构
                                        # 结构: {"cn": {"st":..., "cw": [...]}, "seg_id": ...}
                                        
                                        text = ""
                                        
                                        cn_data = data.get("cn", {})
                                        st_data = cn_data.get("st", {})
                                        type_val = st_data.get("type") # 0:最终结果, 1:中间结果
                                        
                                        st = st_data
                                        if "rt" in st:
                                            for rt in st["rt"]:
                                                for ws_item in rt.get("ws", []):
                                                    for cw in ws_item.get("cw", []):
                                                        if "w" in cw:
                                                            text += cw["w"]
                                        
                                        if text:
                                            print(f"ASR Text: {text}, Type: {type_val}", flush=True)
                                            # 发送给前端，is_final 用于标识是否是句子的最终结果
                                            await callback({"text": text, "is_final": type_val == "0"})
                                            
                                    except Exception as e:
                                        print(f"Error parsing RTASR data: {e}, Raw Data: {data}", flush=True)

                    except Exception as e:
                        print(f"Error receiving from Xunfei: {e}", flush=True)

                # 发送任务
                async def send_audio():
                    try:
                        # 缓冲区，用于积攒到 1280 bytes
                        buffer = bytearray()
                        
                        # 流控变量
                        start_time = time.time()
                        bytes_sent = 0
                        
                        async for chunk in audio_generator:
                            if not chunk: continue
                            
                            buffer.extend(chunk)
                            
                            # 按照 1280 bytes 分片发送
                            while len(buffer) >= AUDIO_FRAME_SIZE:
                                frame = buffer[:AUDIO_FRAME_SIZE]
                                buffer = buffer[AUDIO_FRAME_SIZE:]
                                
                                await ws.send(frame)
                                bytes_sent += len(frame)
                                
                                # 智能流控：仅在发送速度超过实时音频速度时等待
                                # 16k * 16bit * 1ch = 32000 bytes/s
                                expected_time = bytes_sent / 32000.0
                                now = time.time()
                                wait_time = expected_time - (now - start_time)
                                
                                if wait_time > 0.005: # 只有当超前超过 5ms 时才 sleep，避免频繁 sleep
                                    await asyncio.sleep(wait_time)
                        
                        # 发送剩余数据
                        if len(buffer) > 0:
                            await ws.send(buffer)
                            
                        # 发送结束标记
                        await ws.send(b"{\"end\": true}") 
                        print("Sent end signal to Xunfei", flush=True)
                        
                    except Exception as e:
                        print(f"Error sending to Xunfei: {e}", flush=True)

                # 并发运行
                await asyncio.gather(receive_msg(), send_audio())
                
        except Exception as e:
            print(f"ASR Connection failed: {e}", flush=True)
            await callback({"error": str(e)})
