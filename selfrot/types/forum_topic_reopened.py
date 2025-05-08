from typing import Any
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class ForumTopicReopened():
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.any_schema()