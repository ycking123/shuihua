import asyncio
import os
import sys
import websockets
import json
import urllib.parse
from dotenv import load_dotenv

# Add current directory to path so we can import services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.asr_service import XunfeiASRService

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env.local')
load_dotenv(env_path)

APP_ID = os.getenv("XUNFEI_APP_ID")
API_KEY = os.getenv("XUNFEI_API_KEY")
API_SECRET = os.getenv("XUNFEI_API_SECRET")

print(f"Loaded config: APP_ID={APP_ID}, API_KEY={API_KEY[:4]}***, API_SECRET={API_SECRET}")

async def test_connection():
    # Test using the updated XunfeiASRService (Standard IAT)
    
    service = XunfeiASRService(APP_ID, API_KEY, API_SECRET)
    
    url = service.create_url()
    print(f"Generated IAT URL: {url}")
    
    try:
        print("Attempting to connect to Xunfei IAT...")
        # 增加超时时间，禁用 ping
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with websockets.connect(url, ssl=ssl_context, ping_interval=None, open_timeout=20) as ws:
            print("Successfully connected to Xunfei IAT!")
            await asyncio.sleep(1)
            print("Connection maintained.")
    except Exception as e:
        print(f"IAT Connection error: {e}")
        if "401" in str(e):
             print("\n!!! Authentication Failed (401) !!!")
             print("This usually means:")
             print("1. API_SECRET is missing or incorrect.")
             print("2. APP_ID / API_KEY do not match the service.")
             print("Please check your .env.local file.")

if __name__ == "__main__":
    asyncio.run(test_connection())
