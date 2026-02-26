from dataclasses import dataclass

from src.core.config import settings


@dataclass(frozen=True)
class LLMResponse:
    summary: str
    main_py: str
    requirements: list[str]
    dockerfile: str

    def __post_init__(self):
        self._validate_summary()
        self._validate_main_py()
        self._validate_requirements()
        self._validate_dockerfile()

    def _validate_summary(self):
        if not isinstance(self.summary, str) or not self.summary:
            raise ValueError('Invalid summary')

    def _validate_main_py(self):
        if not isinstance(self.main_py, str) or not self.main_py:
            raise ValueError('Invalid main_py')
        if len(self.main_py) > settings.AI_CODEGEN_MAX_MAIN_PY_CHARS:
            raise ValueError('Invalid main_py')

    def _validate_requirements(self):
        if (
            not isinstance(self.requirements, list)
            or not self.requirements
            or not all(isinstance(x, str) for x in self.requirements)
        ):
            raise ValueError('Invalid requirements')
        if len('\n'.join(self.requirements)) > settings.AI_CODEGEN_MAX_REQUIREMENTS_CHARS:
            raise ValueError('Invalid requirements')

    def _validate_dockerfile(self):
        if not isinstance(self.dockerfile, str) or not self.dockerfile:
            raise ValueError('Invalid dockerfile')
        if len(self.dockerfile) > settings.AI_CODEGEN_MAX_DOCKERFILE_CHARS:
            raise ValueError('Invalid dockerfile')
