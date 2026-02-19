import pydantic
from typing import Optional, Type


class AbstractAdv(pydantic.BaseModel):
    title: str
    description: str

    @pydantic.field_validator("title")
    @classmethod
    def title_len(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError("Maximal length of title is 100")
        return v

    @pydantic.field_validator("description")
    @classmethod
    def desc_len(cls, v: str) -> str:
        if len(v) > 1000:
            raise ValueError("Maximal length of description is 1000")
        return v


class CreateAdv(AbstractAdv):
    title: str
    description: str


class UpdateAdv(AbstractAdv):
    title: Optional[str] = None
    description: Optional[str] = None


SCHEMA_CLASS = Type[CreateAdv | UpdateAdv]
SCHEMA = CreateAdv | UpdateAdv