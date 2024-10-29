from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

    # Relationship with Union table (intermediate table for Todo and Tag)
    tags = relationship("Union", back_populates="todo")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    # Relationship with Union table
    todos = relationship("Union", back_populates="tag")

class Union(Base):
    __tablename__ = "union"

    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("todos.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    # Relationship definitions
    todo = relationship("Todo", back_populates="tags")
    tag = relationship("Tag", back_populates="todos")
