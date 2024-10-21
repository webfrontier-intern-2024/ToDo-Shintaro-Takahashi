# Pydanticスキーマ定義
from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str

class Todo(TodoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True

class TodoCreate(TodoBase):
    completed: bool = False  # completed をデフォルトで False に設定