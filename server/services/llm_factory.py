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
        self.model_name = "MiniMaxAI/MiniMax-M2.5"

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
        )
        
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

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




