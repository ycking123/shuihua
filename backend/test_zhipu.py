import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

print("Starting test...", flush=True)

# Load env like in main.py
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
root_env_path = Path(__file__).parent.parent / ".env.local"
load_dotenv(dotenv_path=root_env_path)

API_KEY = os.getenv("ZHIPUAI_API_KEY") or os.getenv("Zhipuai_API_KEY")
print(f"API Key found: {bool(API_KEY)}", flush=True)

if not API_KEY:
    print("No API Key!", flush=True)
    sys.exit(1)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

try:
    print("Calling API...", flush=True)
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    print("Response:", response.choices[0].message.content, flush=True)
except Exception as e:
    print("Error:", e, flush=True)
