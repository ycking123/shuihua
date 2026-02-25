"""测试待办 API 功能"""
import requests

BASE_URL = "http://localhost:8000/api"

print("=" * 60)
print("测试待办 API 功能")
print("=" * 60)

# 1. 测试获取待办列表（按生成时间排序）
print("\n[1] 获取待办列表 - 按生成时间排序")
r = requests.get(f"{BASE_URL}/todos?sort_by=created_at")
print(f"状态码: {r.status_code}")
todos = r.json()
print(f"待办数量: {len(todos)}")
for t in todos[:3]:
    print(f"  - {t['title'][:35]}...")
    print(f"    生成时间: {t['time']} | 会议时间: {t.get('meeting_time', '无')}")

# 2. 测试获取待办列表（按会议时间排序）
print("\n[2] 获取待办列表 - 按会议时间排序")
r = requests.get(f"{BASE_URL}/todos?sort_by=meeting_time")
print(f"状态码: {r.status_code}")
todos = r.json()
print(f"待办数量: {len(todos)}")
for t in todos[:3]:
    print(f"  - {t['title'][:35]}...")
    print(f"    生成时间: {t['time']} | 会议时间: {t.get('meeting_time', '无')}")

# 3. 测试获取会议列表
print("\n[3] 获取会议列表")
r = requests.get(f"{BASE_URL}/meetings")
print(f"状态码: {r.status_code}")
meetings = r.json()
print(f"会议数量: {len(meetings)}")
for m in meetings[:3]:
    print(f"  - {m['title'][:35]}...")
    print(f"    开始时间: {m['start_time']} | 待办数: {m.get('todos_count', 0)}")

# 4. 测试新增待办
if meetings:
    meeting_id = meetings[0]['id']
    print(f"\n[4] 测试新增待办 (关联会议: {meeting_id[:8]}...)")
    
    new_todo = {
        "title": "测试待办事项",
        "content": "这是一个测试待办",
        "priority": "high",
        "type": "meeting",
        "status": "pending",
        "sender": "测试脚本",
        "source_message_id": meeting_id,
        "source_origin": "meeting_minutes"
    }
    
    r = requests.post(f"{BASE_URL}/todos", json=new_todo)
    print(f"状态码: {r.status_code}")
    
    if r.status_code == 200:
        created = r.json()
        todo_id = created['id']
        print(f"✅ 新增成功: {created['title']}")
        print(f"   ID: {todo_id}")
        
        # 5. 测试更新待办
        print(f"\n[5] 测试更新待办")
        update_data = {
            "title": "测试待办事项(已修改)",
            "content": "内容已更新",
            "priority": "urgent"
        }
        r = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
        print(f"状态码: {r.status_code}")
        
        if r.status_code == 200:
            updated = r.json()
            print(f"✅ 更新成功: {updated['title']}")
            print(f"   优先级: {updated['priority']}")
        else:
            print(f"❌ 更新失败: {r.text}")
        
        # 6. 测试删除待办
        print(f"\n[6] 测试删除待办")
        r = requests.delete(f"{BASE_URL}/todos/{todo_id}")
        print(f"状态码: {r.status_code}")
        
        if r.status_code == 200:
            print(f"✅ 删除成功")
        else:
            print(f"❌ 删除失败: {r.text}")
    else:
        print(f"❌ 新增失败: {r.text}")

print("\n" + "=" * 60)
print("测试完成!")
print("=" * 60)

# 7. 测试排序功能
print("\n" + "=" * 60)
print("测试排序功能")
print("=" * 60)

print("\n[按生成时间排序]")
r = requests.get(f"{BASE_URL}/todos?sort_by=created_at")
todos = r.json()
test_todos = [t for t in todos if 'test' in t['title'].lower() or 'product' in t['title'].lower() or 'arch' in t['title'].lower() or 'product'.lower() in t['title'].lower() or 'architect'.lower() in t['title'].lower() or '产品经理' in t['title'] or '架构师' in t['title']]
for t in test_todos[:4]:
    print(f"  - {t['title'][:30]}...")
    print(f"    meeting_time: {t.get('meeting_time', 'None')}")

print("\n[按会议时间排序]")
r = requests.get(f"{BASE_URL}/todos?sort_by=meeting_time")
todos = r.json()
test_todos = [t for t in todos if 'test' in t['title'].lower() or '产品经理' in t['title'] or '架构师' in t['title']]
for t in test_todos[:4]:
    print(f"  - {t['title'][:30]}...")
    print(f"    meeting_time: {t.get('meeting_time', 'None')}")

print("\n说明: 按会议时间排序时，会议时间更晚的应该排在前面")
