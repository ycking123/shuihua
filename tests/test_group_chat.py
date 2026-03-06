# ============================================================================
# 文件: test_group_chat.py
# 模块: tests
# 职责: 企业微信群聊创建功能测试
# ============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import Mock, patch, MagicMock
import json

# 测试意图识别
class TestIntentRecognition(unittest.TestCase):
    """测试意图识别功能"""

    def test_group_chat_intent_keywords(self):
        """测试群聊意图关键词识别"""
        from backend.ai_handler import analyze_intent

        # 模拟客户端
        with patch('backend.ai_handler.client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="group_chat"))]
            mock_client.chat.completions.create.return_value = mock_response

            # 测试各种群聊关键词
            test_cases = [
                "创建群聊 项目讨论群",
                "建个群讨论一下",
                "拉个群",
                "新建群组",
                "创建讨论群 @user1 @user2"
            ]

            for text in test_cases:
                result = analyze_intent(text)
                self.assertEqual(result, "group_chat", f"'{text}' 应识别为 group_chat")

    def test_meeting_intent(self):
        """测试会议意图不被误判"""
        from backend.ai_handler import analyze_intent

        with patch('backend.ai_handler.client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="meeting"))]
            mock_client.chat.completions.create.return_value = mock_response

            result = analyze_intent("安排一个会议")
            self.assertEqual(result, "meeting")

    def test_todo_intent(self):
        """测试待办意图不被误判"""
        from backend.ai_handler import analyze_intent

        with patch('backend.ai_handler.client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="todo"))]
            mock_client.chat.completions.create.return_value = mock_response

            result = analyze_intent("提醒我明天交报告")
            self.assertEqual(result, "todo")

    def test_chat_intent(self):
        """测试闲聊意图"""
        from backend.ai_handler import analyze_intent

        with patch('backend.ai_handler.client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="chat"))]
            mock_client.chat.completions.create.return_value = mock_response

            result = analyze_intent("你好")
            self.assertEqual(result, "chat")


class TestExtractGroupChatInfo(unittest.TestCase):
    """测试群聊信息提取功能"""

    def test_extract_group_info_with_at(self):
        """测试从@符号提取成员"""
        from backend.ai_handler import extract_group_chat_info

        with patch('backend.ai_handler.client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content=json.dumps({
                "chat_name": "项目讨论群",
                "user_ids": ["user1", "user2"]
            })))]
            mock_client.chat.completions.create.return_value = mock_response

            result = extract_group_chat_info("创建群聊 项目讨论群 @user1 @user2")

            self.assertEqual(result["chat_name"], "项目讨论群")
            self.assertIn("user1", result["user_ids"])
            self.assertIn("user2", result["user_ids"])

    def test_extract_group_info_with_members(self):
        """测试从成员列表提取"""
        from backend.ai_handler import extract_group_chat_info

        with patch('backend.ai_handler.client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content=json.dumps({
                "chat_name": "测试群",
                "user_ids": ["zhangsan", "lisi", "wangwu"]
            })))]
            mock_client.chat.completions.create.return_value = mock_response

            result = extract_group_chat_info("创建群聊 测试群\n成员: zhangsan,lisi,wangwu")

            self.assertEqual(result["chat_name"], "测试群")
            self.assertEqual(len(result["user_ids"]), 3)

    def test_extract_group_info_empty(self):
        """测试空输入处理"""
        from backend.ai_handler import extract_group_chat_info

        with patch('backend.ai_handler.client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content=json.dumps({
                "chat_name": "新群聊",
                "user_ids": []
            })))]
            mock_client.chat.completions.create.return_value = mock_response

            result = extract_group_chat_info("创建群聊")

            self.assertEqual(result["chat_name"], "新群聊")
            self.assertEqual(result["user_ids"], [])

    def test_extract_group_info_invalid_json(self):
        """测试无效JSON处理"""
        from backend.ai_handler import extract_group_chat_info

        with patch('backend.ai_handler.client') as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="invalid json"))]
            mock_client.chat.completions.create.return_value = mock_response

            result = extract_group_chat_info("创建群聊")

            self.assertEqual(result["chat_name"], "新群聊")
            self.assertEqual(result["user_ids"], [])


class TestCreateGroupChat(unittest.TestCase):
    """测试群聊创建功能"""

    @patch('backend.server_receive.wechat_client')
    def test_create_group_success(self, mock_client):
        """测试成功创建群聊"""
        from backend.server_receive import create_wecom_group_chat

        # 模拟成功响应
        mock_client.appchat.create.return_value = {"chatid": "wr1234567890"}

        result = create_wecom_group_chat(
            user_ids=["user1", "user2"],
            chat_name="测试群",
            owner="user1"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["chatid"], "wr1234567890")
        self.assertIn("成功", result["message"])

    @patch('backend.server_receive.wechat_client')
    def test_create_group_not_enough_members(self, mock_client):
        """测试成员不足"""
        from backend.server_receive import create_wecom_group_chat

        result = create_wecom_group_chat(
            user_ids=["user1"],
            chat_name="测试群"
        )

        self.assertFalse(result["success"])
        self.assertIn("至少需要2个成员", result["message"])

    @patch('backend.server_receive.wechat_client')
    def test_create_group_no_client(self, mock_client):
        """测试客户端未初始化"""
        from backend.server_receive import create_wecom_group_chat

        # 模拟客户端为None
        with patch('backend.server_receive.wechat_client', None):
            result = create_wecom_group_chat(
                user_ids=["user1", "user2"],
                chat_name="测试群"
            )

        self.assertFalse(result["success"])
        self.assertIn("未初始化", result["message"])

    @patch('backend.server_receive.wechat_client')
    def test_create_group_api_error(self, mock_client):
        """测试API错误处理"""
        from backend.server_receive import create_wecom_group_chat

        # 模拟API错误
        mock_client.appchat.create.side_effect = Exception("60011")

        result = create_wecom_group_chat(
            user_ids=["user1", "user2"],
            chat_name="测试群"
        )

        self.assertFalse(result["success"])
        self.assertIn("可见范围", result["message"])


class TestSendGroupMessage(unittest.TestCase):
    """测试发送群消息功能"""

    @patch('backend.server_receive.wechat_client')
    def test_send_text_message_success(self, mock_client):
        """测试成功发送文本消息"""
        from backend.server_receive import send_wecom_group_message

        result = send_wecom_group_message("wr123456", "测试消息", "text")

        mock_client.appchat.send_text.assert_called_once_with("wr123456", "测试消息")
        self.assertTrue(result)

    @patch('backend.server_receive.wechat_client')
    def test_send_markdown_message(self, mock_client):
        """测试发送markdown消息"""
        from backend.server_receive import send_wecom_group_message

        result = send_wecom_group_message("wr123456", "**测试**", "markdown")

        mock_client.appchat.send_markdown.assert_called_once_with("wr123456", "**测试**")
        self.assertTrue(result)

    @patch('backend.server_receive.wechat_client')
    def test_send_message_no_chatid(self, mock_client):
        """测试空chatid处理"""
        from backend.server_receive import send_wecom_group_message

        result = send_wecom_group_message("", "测试消息")

        self.assertFalse(result)


class TestAPIEndpoints(unittest.TestCase):
    """测试API接口"""

    def test_create_group_request_model(self):
        """测试创建群聊请求模型"""
        from backend.server_receive import CreateGroupChatRequest

        request = CreateGroupChatRequest(
            user_ids=["user1", "user2"],
            chat_name="测试群",
            owner="user1",
            welcome_message="欢迎"
        )

        self.assertEqual(request.user_ids, ["user1", "user2"])
        self.assertEqual(request.chat_name, "测试群")
        self.assertEqual(request.owner, "user1")
        self.assertEqual(request.welcome_message, "欢迎")

    def test_send_message_request_model(self):
        """测试发送消息请求模型"""
        from backend.server_receive import SendGroupMessageRequest

        request = SendGroupMessageRequest(
            chatid="wr123456",
            content="测试",
            msg_type="text"
        )

        self.assertEqual(request.chatid, "wr123456")
        self.assertEqual(request.content, "测试")
        self.assertEqual(request.msg_type, "text")


class TestIntegration(unittest.TestCase):
    """集成测试"""

    @patch('backend.server_receive.create_wecom_group_chat')
    @patch('backend.server_receive.send_wecom_group_message')
    def test_full_group_chat_flow(self, mock_send, mock_create):
        """测试完整群聊创建流程"""
        from backend.server_receive import create_wecom_group_chat_and_notify

        mock_create.return_value = {
            "success": True,
            "chatid": "wr123456",
            "message": "创建成功"
        }

        create_wecom_group_chat_and_notify(
            user_ids=["user1", "user2"],
            chat_name="测试群",
            creator_id="user1",
            source_chat_id="wr789"
        )

        # 验证创建群聊被调用
        mock_create.assert_called_once()
        # 验证发送消息被调用
        mock_send.assert_called()


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestIntentRecognition))
    suite.addTests(loader.loadTestsFromTestCase(TestExtractGroupChatInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestCreateGroupChat))
    suite.addTests(loader.loadTestsFromTestCase(TestSendGroupMessage))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("开始执行企业微信群聊创建功能测试")
    print("=" * 60)

    result = run_tests()

    print("\n" + "=" * 60)
    print("测试执行完成")
    print(f"运行测试数: {result.testsRun}")
    print(f"通过测试数: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败测试数: {len(result.failures)}")
    print(f"错误测试数: {len(result.errors)}")
    print("=" * 60)

    # 返回退出码
    sys.exit(0 if result.wasSuccessful() else 1)
