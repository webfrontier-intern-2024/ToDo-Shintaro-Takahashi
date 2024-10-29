from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table

from sqlalchemy.orm import relationship

from .database import Base



# Association table for Todo and Tag many-to-many relationship

association_table = Table(

    "union", Base.metadata,

    Column("todo_id", Integer, ForeignKey("todos.id")),

    Column("tag_id", Integer, ForeignKey("tags.id"))

)



class Todo(Base):

    __tablename__ = "todos"



    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)

    completed = Column(Boolean, default=False)



    tags = relationship("Tag", secondary=association_table, back_populates="todos")



class Tag(Base):

    __tablename__ = "tags"



    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True, unique=True)



    todos = relationship("Todo", secondary=association_table, back_populates="tags")

