from sqlalchemy.orm import Session, joinedload

from . import models, schemas



# CRUD for Todo

def get_todos(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Todo).options(joinedload(models.Todo.tags)).offset(skip).limit(limit).all()



def get_todo_by_id(db: Session, todo_id: int):

    return db.query(models.Todo).options(joinedload(models.Todo.tags)).filter(models.Todo.id == todo_id).first()



def create_todo(db: Session, todo: schemas.TodoCreate):

    db_todo = models.Todo(title=todo.title, completed=todo.completed)

    db.add(db_todo)

    db.commit()

    db.refresh(db_todo)

    return db_todo



def create_todo_with_tag(db: Session, todo: schemas.TodoCreate, tag_id: int = None):

    db_todo = models.Todo(title=todo.title, completed=todo.completed)

    db.add(db_todo)

    db.commit()

    db.refresh(db_todo)

    if tag_id:

        db_union = models.Union(todo_id=db_todo.id, tag_id=tag_id)

        db.add(db_union)

        db.commit()

        db.refresh(db_union)

    return db_todo



def delete_todo(db: Session, todo_id: int):

    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if db_todo:

        db.delete(db_todo)

        db.commit()

    return db_todo



def update_todo_title(db: Session, todo_id: int, title: str):

    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if db_todo:

        db_todo.title = title

        db.commit()

        db.refresh(db_todo)

    return db_todo



def toggle_complete(db: Session, todo_id: int):

    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if db_todo:

        db_todo.completed = not db_todo.completed  # Toggle completion status

        db.commit()

        db.refresh(db_todo)

    return db_todo



# CRUD for Tag

def get_tags(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Tag).offset(skip).limit(limit).all()



def get_tag_by_id(db: Session, tag_id: int):

    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()



def create_tag(db: Session, tag: schemas.TagCreate):

    db_tag = models.Tag(name=tag.name)

    db.add(db_tag)

    db.commit()

    db.refresh(db_tag)

    return db_tag



def delete_tag(db: Session, tag_id: int):

    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()

    if db_tag:

        db.delete(db_tag)

        db.commit()

    return db_tag



# CRUD for Union (association table)

def create_union(db: Session, todo_id: int, tag_id: int):

    db_union = models.Union(todo_id=todo_id, tag_id=tag_id)

    db.add(db_union)

    db.commit()

    db.refresh(db_union)

    return db_union



def get_unions(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Union).offset(skip).limit(limit).all()



def delete_union(db: Session, union_id: int):

    db_union = db.query(models.Union).filter(models.Union.id == union_id).first()

    if db_union:

        db.delete(db_union)

        db.commit()

    return db_union
