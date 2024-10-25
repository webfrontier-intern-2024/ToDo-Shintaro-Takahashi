# データベースのモデルの定義を行うファイル

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  
 
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

    tags = relationship("Union", back_populates="todo")

class Tag(Base):
    __tablename__ = "tags" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    todos = relationship("Union", back_populates="tag")

class Union(Base):
    __tablename__ = "union"
    
    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("todos.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    # # TodoとTagとの関係を定義
    # todo = relationship("Todo", back_populates="tags")
    # tag = relationship("Tag", back_populates="todos")