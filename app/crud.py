# CRUD操作のロジック
from sqlalchemy.orm import Session
from . import models, schemas

# 既存のtodosを取得するメソッド
def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

# todoを削除するメソッド
def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo

# 特定のtodoをIDで取得するメソッド
def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

# 新しいtodoを作成するメソッド
def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Unionテーブルを使用して、todosとtagsを取得するメソッド
def get_todos_with_tags(db: Session, skip: int = 0, limit: int = 100):
    results = (
        db.query(models.Todo, models.Tag)
        .join(models.Union, models.Todo.id == models.Union.todo_id)
        .join(models.Tag, models.Tag.id == models.Union.tag_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    todos_with_tags = []
    for todo, tag in results:
        todos_with_tags.append({
            "todo_id": todo.id,
            "todo_title": todo.title,
            "tag_id": tag.id,
            "tag_name": tag.name  # 修正：tag.tag -> tag.name（モデル定義と一致させる）
        })
    return todos_with_tags
