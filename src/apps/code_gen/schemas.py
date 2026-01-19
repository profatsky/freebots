import re
from typing import Optional

from pydantic import BaseModel, Field

from src.apps.enums import HandlerType, KeyboardType


class StateSchema(BaseModel):
    name: str


class StatesGroupSchema(BaseModel):
    name: str
    states: list[StateSchema] = Field(default_factory=list)


class HandlerSchema(BaseModel):
    type: HandlerType = Field(default=HandlerType.MESSAGE)
    decorator: Optional[str] = None
    signature: Optional[str] = None
    body: list[str] = Field(default_factory=list)

    def add_to_body(self, code: str):
        code = code.replace("'", '"')
        code = self._process_access_to_user_answers_in_code(code)
        code = self._process_access_to_api_response_in_code(code)
        code = self._process_access_to_username_in_code(code)
        self.body.append(code.strip())

    def _process_access_to_user_answers_in_code(self, code: str) -> str:
        pattern = r'<answers\[(\d+)\]>'

        code = self._format_string_if_pattern_found(pattern, code)

        def replace_match(match):
            return "{answers['answer" + match.group(1) + "']}"

        result = re.sub(pattern, replace_match, code)

        return result

    def _process_access_to_api_response_in_code(self, code: str) -> str:
        pattern = r'<response(.*?)>'

        code = self._format_string_if_pattern_found(pattern, code)

        matches = re.finditer(pattern, code)
        for match in matches:
            response_content = match.group(1).replace('\\"', "'")
            replaced_content = re.sub(r'\[([^\[\]]+)\]', r'.get(\1, {})', response_content)
            code = code.replace(match.group(0), f'{{response_data{replaced_content}}}')

        return code

    def _process_access_to_username_in_code(self, code: str) -> str:
        pattern = r'<username>'

        code = self._format_string_if_pattern_found(pattern, code)

        def replace_match(match):
            if self.type == HandlerType.MESSAGE:
                return '{message.from_user.full_name}'
            else:
                return '{callback.from_user.full_name}'

        result = re.sub(pattern, replace_match, code)

        return result

    @staticmethod
    def _format_string_if_pattern_found(pattern: str, code: str) -> str:
        search_from = 0
        while match := re.search(pattern, code[search_from:]):
            quote_index = code.rfind('"', 0, match.start() + search_from)
            while quote_index != -1 and code[quote_index - 1] != 'f':
                if code[quote_index - 1] == '\\':
                    quote_index = code.rfind('"', 0, quote_index - 1)
                else:
                    code = code[:quote_index] + 'f' + code[quote_index:]
                    search_from += 1
                    break

            search_from += match.end()

        return code


class KeyboardSchema(BaseModel):
    type: KeyboardType
    declaration: str = None
    buttons: list[str] = Field(default_factory=list)

    def add_to_buttons(self, code: str):
        self.buttons.append(code)
