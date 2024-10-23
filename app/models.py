# データベースのモデルの定義を行うファイル

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base  
 
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

class Tag(Base):
    __tablename__ = "tags" 

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, index=True, unique=True)

class Union(Base):
    __tablename__ = "union"

    todo_id = Column(Integer, ForeignKey('todos.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)