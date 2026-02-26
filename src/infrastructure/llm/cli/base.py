from typing import Type, TypeVar, Optional

from src.infrastructure.llm.types import LLMChatMessage

T = TypeVar('T')


class AsyncLLMClient:
    def __init__(self, url: Optional[str] = None, model: Optional[str] = None):
        self.url = url
        self.model = model

    async def make_structured_request(
        self,
        object_type: Type[T],
        history: list[LLMChatMessage],
        model: Optional[str] = None,
        max_tokens: int = 5000,
    ) -> T:
        raise NotImplementedError
