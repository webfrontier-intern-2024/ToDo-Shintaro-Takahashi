# CRUD操作のロジック

from sqlalchemy.orm import Session
from . import models, schemas

# Todoの作成
def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title)
    db.add(db_todo)     # 
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Todoの取得
def get_todos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Todo).offset(skip).limit(limit).all()

# Todoの削除
def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
    return db_todo