# FastAPIアプリケーションのメインファイル

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import create_engine # データベースとの接続をする「エンジン」を作る関数
from sqlalchemy.ext.declarative import declarative_base # DBのテーブルを定義市（SQLAlchemyのベースクラスを作成）
from sqlalchemy.orm import sessionmaker, Session # DBとのセッションを作る関数
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from fastapi.responses import HTMLResponse  



# ここに、指定のデータベースのユザネ、パスワードを指定する
DATABASE_URL = "postgresql://maeda:maedanobu723@localhost/todo_app"

# エンジンの宣言
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# データベースモデルを作成
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@app.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.get("/todos/index", response_class=HTMLResponse)
def read_todos_html(request: Request, db: Session = Depends(get_db)):
    todos = crud.get_todos(db)
    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos})