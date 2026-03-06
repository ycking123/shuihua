# ============================================================================
# 文件: test_glm46_simple.py
# 模块: tests
# 职责: 简单测试 glm-4.6 模型可用性
# ============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ai_handler import client, analyze_intent, extract_group_chat_info


def test_model_connection():
    """测试模型连接"""
    print("=" * 50)
    print("测试1: 模型连接检查")
    print("=" * 50)

    if not client:
        print("❌ 失败: AI 客户端未初始化")
        return False

    print("✅ 客户端已初始化")

    try:
        # 简单调用测试
        response = client.chat.completions.create(
            model="glm-4.6",
            messages=[{"role": "user", "content": "你好"}],
            temperature=0.1,
        )
        print(f"✅ 模型连接成功")
        print(f"   响应: {response.choices[0].message.content[:30]}...")
        return True
    except Exception as e:
        print(f"❌ 模型调用失败: {e}")
        return False


def test_intent_recognition():
    """测试意图识别"""
    print("\n" + "=" * 50)
    print("测试2: 意图识别功能")
    print("=" * 50)

    test_cases = [
        ("创建群聊 项目讨论群 @user1 @user2", "group_chat"),
        ("安排一个明天下午的会议", "meeting"),
        ("提醒我明天交报告", "todo"),
        ("你好，请问今天天气怎么样", "chat"),
    ]

    all_pass = True
    for text, expected in test_cases:
        try:
            result = analyze_intent(text)
            status = "✅" if result == expected else "❌"
            print(f"{status} '{text[:20]}...' -> {result}")
            if result != expected:
                all_pass = False
        except Exception as e:
            print(f"❌ '{text[:20]}...' 出错: {e}")
            all_pass = False

    return all_pass


def test_group_chat_extraction():
    """测试群聊信息提取"""
    print("\n" + "=" * 50)
    print("测试3: 群聊信息提取")
    print("=" * 50)

    test_text = "创建群聊 测试群 @zhangsan @lisi"

    try:
        result = extract_group_chat_info(test_text)
        print(f"✅ 提取成功")
        print(f"   群名称: {result.get('chat_name')}")
        print(f"   成员: {result.get('user_ids')}")
        return True
    except Exception as e:
        print(f"❌ 提取失败: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("glm-4.6 模型简单可用性测试")
    print("=" * 50)

    results = []

    # 运行测试
    results.append(("模型连接", test_model_connection()))
    results.append(("意图识别", test_intent_recognition()))
    results.append(("群聊提取", test_group_chat_extraction()))

    # 汇总结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)

    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status}: {name}")

    all_passed = all(r[1] for r in results)

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！glm-4.6 模型可用")
    else:
        print("⚠️ 部分测试失败，请检查配置")
    print("=" * 50)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
