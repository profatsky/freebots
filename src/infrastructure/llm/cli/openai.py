import json
from typing import TypeVar, Type, Optional

from openai import AsyncOpenAI
from openai.lib._parsing import type_to_response_format_param

from src.core.config import settings
from src.infrastructure.llm.cli.base import AsyncLLMClient
from src.infrastructure.llm.types import LLMChatMessage

T = TypeVar('T')


class AsyncOpenAICli(AsyncLLMClient):
    def __init__(self, url: Optional[str] = None, model: Optional[str] = None):
        super().__init__(url, model)
        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def make_structured_request(
        self,
        object_type: Type[T],
        history: list[LLMChatMessage],
        model: Optional[str] = settings.OPENAI_MODEL,
        max_tokens: int = settings.OPENAI_MAX_TOKENS,
    ) -> T:
        if model is None:
            model = self.model

        json_schema = type_to_response_format_param(object_type)
        response = await self._client.chat.completions.create(
            model=model,
            messages=history,
            max_completion_tokens=max_tokens,
            response_format=json_schema,
        )
        data = json.loads(response.choices[0].message.content)
        return object_type(**data)
