from pydantic import BaseModel



# Pydantic schema for Tag creation

class TagBase(BaseModel):

    name: str



class TagCreate(TagBase):

    pass



class Tag(TagBase):

    id: int



    class Config:

        orm_mode = True



# Pydantic schema for Todo creation and editing

class TodoBase(BaseModel):

    title: str

    completed: bool = False



class TodoCreate(TodoBase):

    pass



class TodoEdit(BaseModel):  # New schema for editing Todo

    title: str



class Todo(TodoBase):

    id: int



    class Config:

        orm_mode = True

