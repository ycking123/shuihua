"""测试后端 API"""
import requests

# 测试会议 API
r = requests.get('http://localhost:3000/api/meetings')
print(f'状态码: {r.status_code}')
d = r.json()
print(f'返回 {len(d)} 条会议')
for m in d[:5]:
    print(f'{m["id"][:8]}... | {m["title"][:40]}')
