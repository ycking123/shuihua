from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import os
import asyncio
try:
    from services.asr_service import XunfeiASRService
except ImportError:
    from ..services.asr_service import XunfeiASRService

router = APIRouter()

@router.websocket("/api/asr")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket client connected for ASR", flush=True)
    
    app_id = os.getenv("XUNFEI_APP_ID", "b051c86c")
    api_key = os.getenv("XUNFEI_API_KEY", "2ef25a95a8608cde7cb75275f07fc5c4")
    api_secret = os.getenv("XUNFEI_API_SECRET", "NDlmYjdmYmNhZDMyNWUyZDg0Mjk0MzI5")
    
    if not app_id or not api_key:
        print("XUNFEI credentials missing (AppID/APIKey)", flush=True)
        await websocket.close(code=1008, reason="Server configuration error")
        return
    
    if not api_secret:
        print("Warning: XUNFEI_API_SECRET is missing. Authentication may fail.", flush=True)

    asr_service = XunfeiASRService(app_id, api_key, api_secret)
    
    # 创建一个队列用于从 WebSocket 接收音频数据并传递给 ASR 服务
    audio_queue = asyncio.Queue()
    
    async def audio_generator():
        while True:
            data = await audio_queue.get()
            if data is None: # 结束信号
                break
            yield data

    async def send_result_to_client(result):
        try:
            await websocket.send_json(result)
        except Exception as e:
            print(f"Error sending result to client: {e}", flush=True)

    # 启动 ASR 服务任务
    asr_task = asyncio.create_task(asr_service.stream_audio(audio_generator(), send_result_to_client))

    try:
        while True:
            # 接收前端传来的消息（可能是二进制音频，也可能是文本控制指令）
            message = await websocket.receive()
            
            if "bytes" in message:
                data = message["bytes"]
                if len(data) > 0:
                     await audio_queue.put(data)
            elif "text" in message:
                text = message["text"]
                if text == "STOP":
                    print("Received STOP signal from client", flush=True)
                    await audio_queue.put(None) # 发送结束信号给 ASR 服务
                    # 继续循环，等待接收 ASR 结果并发送给前端，直到连接关闭
                else:
                    print(f"Received unknown text: {text}", flush=True)
            
    except WebSocketDisconnect:
        print("Client disconnected", flush=True)
        await audio_queue.put(None) # 停止 generator
    except Exception as e:
        print(f"WebSocket error: {e}", flush=True)
        await audio_queue.put(None)
    finally:
        # 等待 ASR 任务结束
        await asr_task

