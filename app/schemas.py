# Pydanticスキーマ定義
from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
class TodoCreate(TodoBase):
    completed: bool = False
class Todo(TodoBase):
    id: int
    completed: bool
    class Config:
        orm_mode = True

class TagBase(BaseModel):
    tag: str
class TagCreate(TagBase):
    pass
class Tag(TagBase):
    id: int
    class Config:
        orm_mode = True

class UnionBase(BaseModel):
    todo_id: int
    tag_id: int
class UnionCreate(UnionBase):
    pass
class Union(UnionBase):
    class Config:
        orm_mode = True