from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, AsyncGenerator, Optional
import os


@dataclass
class Message:
    role: str
    content: str


@dataclass
class LLMResponse:
    content: str
    usage: Optional[dict] = None
    model: str = ""
    finish_reason: str = ""


class LLMProvider(ABC):
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> LLMResponse:
        pass

    @abstractmethod
    async def stream_chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    async def close(self):
        pass


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str = None, base_url: str = None):
        from anthropic import AsyncAnthropic
        self.client = AsyncAnthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
            base_url=base_url,
        )

    async def chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> LLMResponse:
        system_msg = ""
        filtered_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                filtered_messages.append({"role": msg.role, "content": msg.content})

        response = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_msg,
            messages=filtered_messages,
        )

        return LLMResponse(
            content=response.content[0].text,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            model=model,
            finish_reason=response.stop_reason or "stop",
        )

    async def stream_chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        system_msg = ""
        filtered_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                filtered_messages.append({"role": msg.role, "content": msg.content})

        stream = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_msg,
            messages=filtered_messages,
            stream=True,
        )

        async for chunk in stream:
            if chunk.type == "content_block_delta":
                yield chunk.delta.text

    async def close(self):
        await self.client.close()


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str = None, base_url: str = None):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url,
        )

    async def chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> LLMResponse:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return LLMResponse(
            content=response.choices[0].message.content,
            usage={
                "input_tokens": response.usage.prompt_tokens if response.usage else 0,
                "output_tokens": response.usage.completion_tokens if response.usage else 0,
            },
            model=model,
            finish_reason=response.choices[0].finish_reason or "stop",
        )

    async def stream_chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def close(self):
        await self.client.close()


class OpenRouterProvider(LLMProvider):
    def __init__(self, api_key: str = None, base_url: str = None):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(
            api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
            base_url=base_url or "https://openrouter.ai/api/v1",
        )

    async def chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> LLMResponse:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            max_tokens=max_tokens,
            temperature=temperature,
            extra_headers={
                "HTTP-Referer": "https://github.com/modelx/modelx-voice",
                "X-Title": "ModelX Voice Assistant",
            },
        )

        return LLMResponse(
            content=response.choices[0].message.content,
            usage={
                "input_tokens": response.usage.prompt_tokens if response.usage else 0,
                "output_tokens": response.usage.completion_tokens if response.usage else 0,
            },
            model=model,
            finish_reason=response.choices[0].finish_reason or "stop",
        )

    async def stream_chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
            extra_headers={
                "HTTP-Referer": "https://github.com/modelx/modelx-voice",
                "X-Title": "ModelX Voice Assistant",
            },
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def close(self):
        await self.client.close()


class OllamaProvider(LLMProvider):
    def __init__(self, api_key: str = None, base_url: str = None):
        import httpx
        self.base_url = base_url or "http://localhost:11434"
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=120.0)

    async def chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> LLMResponse:
        response = await self.client.post(
            "/api/chat",
            json={
                "model": model,
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                },
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()

        return LLMResponse(
            content=data["message"]["content"],
            usage={
                "input_tokens": data.get("prompt_eval_count", 0),
                "output_tokens": data.get("eval_count", 0),
            },
            model=model,
            finish_reason=data.get("done_reason", "stop"),
        )

    async def stream_chat_completion(
        self,
        messages: List[Message],
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        async with self.client.stream(
            "POST",
            "/api/chat",
            json={
                "model": model,
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                },
                "stream": True,
            },
            timeout=120.0,
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    import json
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]

    async def close(self):
        await self.client.aclose()


_PROVIDERS = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "openrouter": OpenRouterProvider,
    "ollama": OllamaProvider,
}

_DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-20250514",
    "openai": "gpt-4o",
    "openrouter": "anthropic/claude-sonnet-4",
    "ollama": "llama3.2",
}


def get_provider(name: str, api_key: str = None, base_url: str = None) -> LLMProvider:
    if name not in _PROVIDERS:
        raise ValueError(f"Unknown provider: {name}. Available: {list(_PROVIDERS.keys())}")
    return _PROVIDERS[name](api_key, base_url)


def get_default_model(provider: str) -> str:
    return _DEFAULT_MODELS.get(provider, "claude-sonnet-4-20250514")


def list_providers() -> List[str]:
    return list(_PROVIDERS.keys())