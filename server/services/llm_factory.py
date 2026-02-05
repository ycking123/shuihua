from abc import ABC, abstractmethod
from typing import List, Generator, Any
import os
from zhipuai import ZhipuAI

class LLMProvider(ABC):
    @abstractmethod
    def list_models(self) -> List[str]:
        """List available models for this provider."""
        pass

    @abstractmethod
    def chat_stream(self, model: str, messages: List[dict], system_instruction: str = None) -> Generator[Any, None, None]:
        """Stream chat response."""
        pass

class ZhipuProvider(LLMProvider):
    def __init__(self):
        self.api_key = os.getenv("ZHIPUAI_API_KEY") or os.getenv("LOCAL_ZHIPU_APIKEY")
        if not self.api_key:
            raise ValueError("ZHIPUAI_API_KEY not configured")
        self.client = ZhipuAI(api_key=self.api_key)
        self.available_models = ["glm-4-flash", "glm-4", "glm-4-plus", "glm-4-air", "glm-4-airx"]

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
        except Exception as e:
            print(f"Error initializing ZhipuProvider: {e}")
            
        return models

