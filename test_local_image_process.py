
import os
import base64
import requests
import json
from pathlib import Path

# 配置
BACKEND_URL = "http://localhost:8080/wecom/callback"
# 模拟一张本地图片（你可以手动放一张图片到这里，或者我们生成一个假的 base64）
# 为了演示，我们先尝试读取一个本地图片文件。如果没有，请提供一个图片路径。
# 这里假设用户在项目根目录下放了一个 `test_image.jpg`，如果没有，脚本会创建一个简单的纯色图片。

TEST_IMAGE_PATH = Path("test_image.jpg")

def create_dummy_image():
    """创建一个简单的测试图片 (红色 100x100)"""
    # 这是一个 1x1 红色像素的 PNG 图片的 base64
    # 实际上为了让 AI 能识别，最好是一张真实的聊天截图。
    # 这里我们只是为了测试数据流（server_receive 接收图片 -> 解码 -> AI -> 推送）
    # 如果没有真实图片，AI 可能无法识别出内容，但流程会跑通。
    print("⚠️ 未找到 test_image.jpg，正在生成一个简单的测试图片...")
    from PIL import Image
    img = Image.new('RGB', (800, 600), color = (73, 109, 137))
    img.save(TEST_IMAGE_PATH)
    print(f"✅ 已生成测试图片: {TEST_IMAGE_PATH}")

def simulate_wechat_image_msg(image_path):
    # 1. 读取图片并转为 base64 (模拟企业微信下载后的内容)
    # 注意：真实的 wecom/callback 接收的是 XML 消息，里面包含 MediaId。
    # 后端 server_receive 会拿着 MediaId 去企业微信服务器下载图片。
    # **关键问题**：我们本地无法让 server_receive 去真的下载一个假的 MediaId。
    #
    # **解决方案**：
    # 为了测试“本地图片 -> AI -> 待办”的流程，我们不能直接调用 wecom/callback 接口，
    # 因为那个接口依赖真实的微信服务器来下载图片。
    # 
    # 我们应该直接调用 backend.ai_handler 中的处理逻辑，或者模拟一个新的测试接口。
    # 但为了最接近真实环境，我们可以写一个脚本，直接调用 `process_image_sync` 函数的核心逻辑，
    # 只是跳过“从微信下载”这一步，直接注入本地图片数据。
    
    print(f"📸 读取图片: {image_path}")
    with open(image_path, "rb") as img_file:
        image_content = img_file.read()
    
    base64_data = base64.b64encode(image_content).decode('utf-8')
    
    # 2. 直接调用 AI 处理函数 (模拟 server_receive 中的逻辑)
    print("🚀 开始模拟后端处理流程...")
    
    # 动态导入后端函数
    import sys
    # 确保能找到 backend 模块
    sys.path.append(os.getcwd())
    
    try:
        from backend.ai_handler import analyze_chat_screenshot_with_glm4v, parse_ai_result_to_todos, process_ai_result_and_push
        
        # 3. 调用 AI 分析
        print("🤖 调用 AI 分析 (这可能需要几秒钟)...")
        json_result = analyze_chat_screenshot_with_glm4v(base64_data)
        
        if json_result:
            print("✅ AI 分析成功，结果如下:")
            print(json_result)
            
            # 4. 解析并推送到后端 (注意：ai_handler 中已经更新为推送给 8080)
            print("🔄 正在解析并推送到本地后端 (Port 8080)...")
            
            # 方式 A: 使用 process_ai_result_and_push (它内部会发 HTTP 请求)
            success = process_ai_result_and_push(json_result)
            
            if success:
                print("🎉 测试通过！待办事项已推送到前端。")
            else:
                print("❌ 推送失败，请检查后端日志。")
        else:
            print("⚠️ AI 未返回有效结果 (可能是图片内容无法识别)")
            
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在项目根目录下运行此脚本，并且已安装所有依赖。")
    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    if not TEST_IMAGE_PATH.exists():
        # 尝试创建一个简单的图，或者提示用户
        # create_dummy_image() # 需要 PIL，为了不引入额外依赖，建议用户提供图片
        print(f"❌ 请在当前目录下放置一张名为 '{TEST_IMAGE_PATH}' 的聊天截图用于测试。")
    else:
        simulate_wechat_image_msg(TEST_IMAGE_PATH)
