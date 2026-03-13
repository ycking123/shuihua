from abc import ABC, abstractmethod
from typing import List, Generator, Any
import os
from zhipuai import ZhipuAI
from openai import OpenAI

class LLMProvider(ABC):
    @abstractmethod
    def list_models(self) -> List[str]:
        """List available models for this provider."""
        pass

    @abstractmethod
    def chat_stream(self, model: str, messages: List[dict], system_instruction: str = None) -> Generator[Any, None, None]:
        """Stream chat response."""
        pass

class QwenProvider(LLMProvider):
    """Qwen 模型提供商，通过 shuihua.ai API 调用"""
    def __init__(self):
        api_key = os.getenv("QWEN_API_KEY", "sk-Bh3wSeeq_LJOHUYyfKus6Q")
        self.client = OpenAI(
            api_key=api_key, 
            base_url="https://api.shuihua.ai/v1"
        )
        self.model_name = "Qwen/Qwen3.5-397B-A17B-FP8"

    def list_models(self) -> List[str]:
        return [self.model_name]

    def chat_stream(self, model: str, messages: List[dict], system_instruction: str = None) -> Generator[Any, None, None]:
        final_messages = []
        if system_instruction:
            final_messages.append({"role": "system", "content": system_instruction})
        
        final_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=model,
            messages=final_messages,
            stream=True,
            max_tokens=2048,
            extra_body={"include_reasoning": False}
        )
        
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class ZhipuProvider(LLMProvider):
    def __init__(self):
        self.api_key = os.getenv("ZHIPUAI_API_KEY") or os.getenv("LOCAL_ZHIPU_APIKEY")
        if not self.api_key:
            raise ValueError("ZHIPUAI_API_KEY not configured")
        self.client = ZhipuAI(api_key=self.api_key)
        self.available_models = ["glm-4.6", "glm-4-flash", "glm-4", "glm-4-plus", "glm-4-air", "glm-4-airx"]

    def list_models(self) -> List[str]:
        return self.available_models

    def chat_stream(self, model: str, messages: List[dict], system_instruction: str = None) -> Generator[Any, None, None]:
        final_messages = []
        if system_instruction:
            final_messages.append({"role": "system", "content": system_instruction})
        
        final_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=model,
            messages=final_messages,
            stream=True,
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class MiniMaxProvider(LLMProvider):
    """MiniMax 模型提供商，通过 shuihua.ai API 调用"""
    def __init__(self):
        api_key = os.getenv("MINIMAX_API_KEY", "sk-Bh3wSeeq_LJOHUYyfKus6Q")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.shuihua.ai/v1"
        )
        self.models = ["MiniMaxAI/MiniMax-M2.5", "MiniMaxAI/MiniMax-M2.5-fast"]

    def list_models(self) -> List[str]:
        return self.models

    def chat_stream(self, model: str, messages: List[dict], system_instruction: str = None) -> Generator[Any, None, None]:
        is_fast = "fast" in model
        if is_fast:
            fast_prompt = "【极速模式指令】请直接输出最终回答，严禁进行内部推演或输出思考过程，绝不允许使用<think>标签。"
            if system_instruction:
                system_instruction = f"{fast_prompt}\n{system_instruction}"
            else:
                system_instruction = fast_prompt

        final_messages = []
        if system_instruction:
            final_messages.append({"role": "system", "content": system_instruction})
        
        final_messages.extend(messages)

        actual_model = "MiniMaxAI/MiniMax-M2.5"
        
        kwargs = {
            "model": actual_model,
            "messages": final_messages,
            "stream": True,
            "max_tokens": 2048,
        }
        
        if is_fast:
            # 暴力尝试关闭目前主流兼容接口的所有思考参数
            kwargs["extra_body"] = {
                "include_reasoning": False,
                "reasoning_effort": "low",
                "thinking": False,
                "with_reasoning": False
            }

        response = self.client.chat.completions.create(**kwargs)
        
        in_think_block = False
        think_buffer = ""
        
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                
                # 如果是极速模式，在此处强行拦截并丢弃 <think> 过程
                if is_fast:
                    think_buffer += content
                    # 动态检测是否含有 think 标签
                    if not in_think_block:
                        if "<think>" in think_buffer:
                            # 刚进入 think 块，把 <think> 之前的内容放行
                            parts = think_buffer.split("<think>")
                            if parts[0]:
                                yield parts[0]
                            in_think_block = True
                            # 保留 <think> 之后的内容等待 </think>
                            think_buffer = parts[1] if len(parts) > 1 else ""
                        else:
                            # 没有进入 think 块，安全放行（保留不到7个可能形成<think>的尾部字符防止截断）
                            if len(think_buffer) > 7:
                                safe_str = think_buffer[:-7]
                                think_buffer = think_buffer[-7:]
                                yield safe_str
                    else:
                        # 正在 think 块中，等待退出标签
                        if "</think>" in think_buffer:
                            parts = think_buffer.split("</think>")
                            in_think_block = False
                            think_buffer = parts[1] if len(parts) > 1 else ""
                            # 退出后如果有残留也先不释放，等下一次循环
                            
                else:
                    yield content
                    
        # 兜底释放
        if is_fast and not in_think_block and think_buffer:
            # 防止最后带有半拉子标签
            if "<think" not in think_buffer:
                yield think_buffer


class LLMFactory:
    _providers = {}

    @classmethod
    def register_provider(cls, name: str, provider_cls):
        cls._providers[name] = provider_cls

    @classmethod
    def get_provider(cls, model_name: str) -> LLMProvider:
        # Simple logic: if model starts with glm, use Zhipu. 
        # In a more complex setup, we might have a specific mapping or default provider.
        if model_name.startswith("glm"):
            return ZhipuProvider()
        
        if model_name.startswith("Qwen"):
            return QwenProvider()
        
        if model_name.startswith("MiniMax"):
            return MiniMaxProvider()
        
        # Default to Zhipu for now if unknown, or raise error
        # Ideally we check which provider supports the model
        return ZhipuProvider()

    @classmethod
    def get_all_models(cls) -> List[dict]:
        """Return a list of all models from all providers."""
        models = []
        # Instantiate providers to get their models
        # Currently we only have Zhipu
        try:
            zhipu = ZhipuProvider()
            for m in zhipu.list_models():
                models.append({"id": m, "name": m, "provider": "Zhipu AI"})
            print(f"✅ ZhipuProvider 加载成功，模型数: {len(zhipu.list_models())}")
        except Exception as e:
            print(f"⚠️ ZhipuProvider 初始化失败（智谱模型不可用）: {e}")
            print(f"   请检查环境变量 ZHIPUAI_API_KEY 或 LOCAL_ZHIPU_APIKEY 是否已配置")
            
        try:
            qwen = QwenProvider()
            for m in qwen.list_models():
                models.append({"id": m, "name": m, "provider": "Qwen"})
        except Exception as e:
            print(f"Error initializing QwenProvider: {e}")
        
        try:
            minimax = MiniMaxProvider()
            for m in minimax.list_models():
                models.append({"id": m, "name": m, "provider": "MiniMax"})
        except Exception as e:
            print(f"Error initializing MiniMaxProvider: {e}")
            
        return models




