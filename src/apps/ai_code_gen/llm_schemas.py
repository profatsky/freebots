from pydantic import BaseModel


class AICodeGenLLMResponse(BaseModel):
    summary: str
    main_py: str
    requirements: list[str]
    dockerfile: str
