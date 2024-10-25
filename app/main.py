from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from fastapi.responses import HTMLResponse  
import urllib.parse  # 追加：パスワードのエスケープに使用

# パスワードをエスケープ
password = urllib.parse.quote_plus("rH8,KeGa")
DATABASE_URL = f"postgresql://codeserver:{password}@localhost/todo_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=engine)

# 基本のルート
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Todoを作成するエンドポイント
@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

# Todos一覧を取得するエンドポイント
@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

# Todoを削除するエンドポイント
@app.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.get("/todos/index", response_class=HTMLResponse)
def read_todos_html(request: Request, db: Session = Depends(get_db)):
    todos_with_tags = crud.get_todos_with_tags(db)
    if not todos_with_tags:
        print("No todos found or error occurred")
    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos_with_tags})


# TodosをクリアするHTML用エンドポイント
@app.get("/todos/clear", response_class=HTMLResponse)
def read_todos_html(request: Request, db: Session = Depends(get_db)):
    todos = crud.get_todos(db)
    return templates.TemplateResponse("clear.html", {"request": request, "todos": todos})

# Todoの完了ステータスをトグル（変更）するエンドポイント
@app.put("/todos/{todo_id}/toggle", response_model=schemas.Todo)
def toggle_todo_completion(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo_by_id(db, todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.completed = not db_todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Unionを使用して、TodosとTagsの関係を取得するエンドポイント
@app.get("/todos_with_tags/", response_model=List[dict])
def read_todos_with_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos_with_tags = crud.get_todos_with_tags(db, skip=skip, limit=limit)
    return todos_with_tags

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
