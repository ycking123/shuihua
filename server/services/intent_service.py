"""
意图识别与参数提取服务
使用LLM进行智能意图识别和参数提取
支持多轮对话参数收集
"""

import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from ..services.llm_factory import LLMFactory


# 意图定义
INTENTS = {
    "meeting": "创建会议",
    "group": "创建群聊",
    "todo": "创建待办",
    "chat": "普通聊天"
}

# 各意图的必填参数
REQUIRED_PARAMS = {
    "meeting": ["title", "start_time", "participants"],
    "group": ["group_name", "members"],
    "todo": ["title", "owner"]
}

# 参数中文名称映射
PARAM_NAMES_CN = {
    "title": "会议主题",
    "start_time": "会议时间",
    "end_time": "结束时间",
    "participants": "参会人员",
    "location": "会议地点",
    "group_name": "群聊名称",
    "members": "群成员",
    "owner": "负责人",
    "priority": "优先级",
    "description": "描述"
}


class IntentService:
    """意图识别服务"""
    
    def __init__(self):
        self.provider = LLMFactory.get_provider("MiniMaxAI/MiniMax-M2.5")
        self.model_name = "MiniMaxAI/MiniMax-M2.5"
    
    def detect_intent(self, user_input: str, context_messages: List[Dict] = None) -> Dict[str, Any]:
        """
        检测用户意图
        返回: {"intent": "meeting/group/todo/chat", "confidence": float}
        """
        system_prompt = """
你是一个智能意图识别助手。请分析用户的输入，判断用户的意图。

可选意图：
1. meeting - 创建会议（关键词：开会、会议、讨论、约个会、schedule meeting）
2. group - 创建群聊（关键词：建群、拉群、群聊、创建群组、create group）
3. todo - 创建待办（关键词：待办、任务、提醒、要做、todo、task、remind）
4. chat - 普通聊天（以上都不是）

请只返回JSON格式：
{"intent": "meeting/group/todo/chat", "confidence": 0-1之间的数值}

注意：
- 如果用户说"帮我创建会议"、"开个会"等，意图是 meeting
- 如果用户说"拉个群"、"建个群聊"等，意图是 group
- 如果用户说"添加待办"、"提醒我"等，意图是 todo
- 其他情况意图是 chat
"""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加上下文
        if context_messages:
            for msg in context_messages[-3:]:  # 最近3条
                messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.provider.chat_stream(
                model=self.model_name,
                messages=messages
            )
            
            # 收集流式响应
            result = ""
            for chunk in response:
                result += chunk
            
            # 解析JSON
            match = re.search(r'\{.*\}', result, re.DOTALL)
            if match:
                intent_data = json.loads(match.group())
                return intent_data
            
            # 默认返回chat
            return {"intent": "chat", "confidence": 1.0}
            
        except Exception as e:
            print(f"❌ 意图识别失败: {e}")
            return {"intent": "chat", "confidence": 1.0}
    
    def extract_params_with_llm(self, user_input: str, intent: str, 
                                 existing_params: Dict = None,
                                 context_messages: List[Dict] = None) -> Dict[str, Any]:
        """
        使用LLM从用户输入中提取参数
        """
        if intent == "meeting":
            return self._extract_meeting_params(user_input, existing_params, context_messages)
        elif intent == "group":
            return self._extract_group_params(user_input, existing_params, context_messages)
        elif intent == "todo":
            return self._extract_todo_params(user_input, existing_params, context_messages)
        else:
            return {}
    
    def _extract_meeting_params(self, user_input: str, existing_params: Dict = None,
                                 context_messages: List[Dict] = None) -> Dict[str, Any]:
        """提取会议参数"""
        
        system_prompt = """
你是一个智能参数提取助手。请从用户输入中提取会议相关信息。

需要提取的字段：
- title: 会议主题/标题（必填）
- start_time: 会议时间（必填，如：明天下午3点、2024-01-15 14:00）
- end_time: 结束时间（可选）
- participants: 参会人员列表（必填，如：["张三", "李四"]）
- location: 会议地点（可选）
- description: 会议描述（可选）

请只返回JSON格式，不要有多余文字：
{
    "title": "会议主题",
    "start_time": "时间描述",
    "end_time": "结束时间",
    "participants": ["人员1", "人员2"],
    "location": "地点",
    "description": "描述"
}

注意：
1. 如果某个字段没有提到，不要猜测，设为null或空数组
2. 时间保持用户原始描述，不要转换
3. 人员要提取具体姓名，用逗号、空格或"和"分隔的都分开
4. 如果用户说"我"，保留"我"这个字
"""
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        context_str = ""
        if context_messages:
            for msg in context_messages[-5:]:
                role = "用户" if msg.get("role") == "user" else "助手"
                context_str += f"{role}: {msg.get('content', '')}\n"
        
        existing_str = ""
        if existing_params:
            existing_str = f"\n已收集的参数：{json.dumps(existing_params, ensure_ascii=False)}"
        
        messages = [
            {"role": "system", "content": f"{system_prompt}\n\n当前时间：{current_time}{existing_str}"}
        ]
        
        if context_str:
            messages.append({"role": "system", "content": f"对话上下文：\n{context_str}"})
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.provider.chat_stream(
                model=self.model_name,
                messages=messages
            )
            
            result = ""
            for chunk in response:
                result += chunk
            
            # 清理和解析JSON
            result = self._clean_json_response(result)
            match = re.search(r'\{.*\}', result, re.DOTALL)
            
            if match:
                params = json.loads(match.group())
                # 过滤掉null值
                return {k: v for k, v in params.items() if v is not None and v != [] and v != ""}
            
            return {}
            
        except Exception as e:
            print(f"❌ 会议参数提取失败: {e}")
            return {}
    
    def _extract_group_params(self, user_input: str, existing_params: Dict = None,
                               context_messages: List[Dict] = None) -> Dict[str, Any]:
        """提取群聊参数"""
        
        system_prompt = """
你是一个智能参数提取助手。请从用户输入中提取群聊相关信息。

需要提取的字段：
- group_name: 群聊名称（必填）
- members: 群成员列表（必填，如：["张三", "李四"]）
- description: 群描述（可选）

请只返回JSON格式，不要有多余文字：
{
    "group_name": "群聊名称",
    "members": ["成员1", "成员2"],
    "description": "描述"
}

注意：
1. 如果某个字段没有提到，不要猜测，设为null或空数组
2. 人员要提取具体姓名，用逗号、空格或"和"分隔的都分开
3. 如果用户说"我"，保留"我"这个字
"""
        
        context_str = ""
        if context_messages:
            for msg in context_messages[-5:]:
                role = "用户" if msg.get("role") == "user" else "助手"
                context_str += f"{role}: {msg.get('content', '')}\n"
        
        existing_str = ""
        if existing_params:
            existing_str = f"\n已收集的参数：{json.dumps(existing_params, ensure_ascii=False)}"
        
        messages = [
            {"role": "system", "content": f"{system_prompt}{existing_str}"}
        ]
        
        if context_str:
            messages.append({"role": "system", "content": f"对话上下文：\n{context_str}"})
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.provider.chat_stream(
                model=self.model_name,
                messages=messages
            )
            
            result = ""
            for chunk in response:
                result += chunk
            
            result = self._clean_json_response(result)
            match = re.search(r'\{.*\}', result, re.DOTALL)
            
            if match:
                params = json.loads(match.group())
                return {k: v for k, v in params.items() if v is not None and v != [] and v != ""}
            
            return {}
            
        except Exception as e:
            print(f"❌ 群聊参数提取失败: {e}")
            return {}
    
    def _extract_todo_params(self, user_input: str, existing_params: Dict = None,
                              context_messages: List[Dict] = None) -> Dict[str, Any]:
        """提取待办参数"""
        
        system_prompt = """
你是一个智能参数提取助手。请从用户输入中提取待办事项相关信息。

需要提取的字段：
- title: 待办标题（必填）
- owner: 负责人（必填，如：我、张三、李四）
- due_date: 截止日期（可选，如：明天、本周五、2024-01-15）
- priority: 优先级（可选：紧急、高、中、低）
- description: 描述（可选）

请只返回JSON格式，不要有多余文字：
{
    "title": "待办标题",
    "owner": "负责人",
    "due_date": "截止日期",
    "priority": "优先级",
    "description": "描述"
}

注意：
1. 如果某个字段没有提到，不要猜测，设为null
2. 时间保持用户原始描述，不要转换
3. 如果用户说"我"，保留"我"这个字
4. 优先级映射：紧急/urgent -> 紧急，高/high/重要 -> 高，中/medium/普通 -> 中，低/low -> 低
"""
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        context_str = ""
        if context_messages:
            for msg in context_messages[-5:]:
                role = "用户" if msg.get("role") == "user" else "助手"
                context_str += f"{role}: {msg.get('content', '')}\n"
        
        existing_str = ""
        if existing_params:
            existing_str = f"\n已收集的参数：{json.dumps(existing_params, ensure_ascii=False)}"
        
        messages = [
            {"role": "system", "content": f"{system_prompt}\n\n当前时间：{current_time}{existing_str}"}
        ]
        
        if context_str:
            messages.append({"role": "system", "content": f"对话上下文：\n{context_str}"})
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.provider.chat_stream(
                model=self.model_name,
                messages=messages
            )
            
            result = ""
            for chunk in response:
                result += chunk
            
            result = self._clean_json_response(result)
            match = re.search(r'\{.*\}', result, re.DOTALL)
            
            if match:
                params = json.loads(match.group())
                return {k: v for k, v in params.items() if v is not None and v != ""}
            
            return {}
            
        except Exception as e:
            print(f"❌ 待办参数提取失败: {e}")
            return {}
    
    def _clean_json_response(self, response: str) -> str:
        """清理LLM返回的JSON响应"""
        # 移除markdown代码块标记
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        return response.strip()
    
    def generate_clarification_question(self, missing_params: List[str], 
                                         collected_params: Dict,
                                         intent: str) -> str:
        """生成追问问题"""
        missing_names = [PARAM_NAMES_CN.get(p, p) for p in missing_params]
        
        # 先显示已收集的信息
        question_parts = []
        
        if intent == "meeting":
            if collected_params.get("title"):
                question_parts.append(f"会议主题：{collected_params['title']}")
            if collected_params.get("start_time"):
                question_parts.append(f"时间：{collected_params['start_time']}")
            if collected_params.get("participants"):
                participants = collected_params["participants"]
                if isinstance(participants, list):
                    question_parts.append(f"参会人：{'、'.join(participants)}")
                else:
                    question_parts.append(f"参会人：{participants}")
        
        elif intent == "group":
            if collected_params.get("group_name"):
                question_parts.append(f"群聊名称：{collected_params['group_name']}")
            if collected_params.get("members"):
                members = collected_params["members"]
                if isinstance(members, list):
                    question_parts.append(f"成员：{'、'.join(members)}")
                else:
                    question_parts.append(f"成员：{members}")
        
        elif intent == "todo":
            if collected_params.get("title"):
                question_parts.append(f"待办：{collected_params['title']}")
            if collected_params.get("owner"):
                question_parts.append(f"负责人：{collected_params['owner']}")
        
        # 构建问题
        if question_parts:
            question = "已记录信息：\n" + "\n".join([f"• {p}" for p in question_parts])
            question += f"\n\n还缺少：{', '.join(missing_names)}\n请补充。"
        else:
            question = f"请提供以下信息：{', '.join(missing_names)}"
        
        return question
    
    def generate_confirmation_prompt(self, intent: str, params: Dict) -> str:
        """生成确认提示"""
        if intent == "meeting":
            prompt = "请确认以下会议信息：\n"
            prompt += f"📅 主题：{params.get('title')}\n"
            prompt += f"⏰ 时间：{params.get('start_time')}\n"
            participants = params.get('participants', [])
            if isinstance(participants, list):
                prompt += f"👥 参会人：{'、'.join(participants)}\n"
            else:
                prompt += f"👥 参会人：{participants}\n"
            if params.get('location'):
                prompt += f"📍 地点：{params['location']}\n"
            prompt += '\n是否创建会议？（确认请回复"是"或"确认"）'
        
        elif intent == "group":
            prompt = "请确认以下群聊信息：\n"
            prompt += f"💬 群聊名称：{params.get('group_name')}\n"
            members = params.get('members', [])
            if isinstance(members, list):
                prompt += f"👥 成员：{'、'.join(members)}\n"
            else:
                prompt += f"👥 成员：{members}\n"
            prompt += '\n是否创建群聊？（确认请回复"是"或"确认"）'
        
        elif intent == "todo":
            prompt = "请确认以下待办信息：\n"
            prompt += f"📝 待办：{params.get('title')}\n"
            prompt += f"👤 负责人：{params.get('owner')}\n"
            if params.get('due_date'):
                prompt += f"📅 截止日期：{params['due_date']}\n"
            if params.get('priority'):
                prompt += f"⚡ 优先级：{params['priority']}\n"
            prompt += '\n是否创建待办？（确认请回复"是"或"确认"）'
        
        else:
            prompt = "参数已收集完整，是否执行？"
        
        return prompt


# 全局意图服务实例
intent_service = IntentService()

