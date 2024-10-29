from fastapi import FastAPI, Depends, HTTPException, Request, Form, Body

from sqlalchemy.orm import Session

from . import crud, models, schemas

from .database import SessionLocal, engine, get_db

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

from fastapi.responses import JSONResponse, RedirectResponse

from typing import List, Optional

from fastapi.responses import HTMLResponse

import os



# Initialize FastAPI application

app = FastAPI()



# Set up templates and static files

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")



# Create database tables

models.Base.metadata.create_all(bind=engine)



# Todo routes

@app.get("/", response_class=HTMLResponse)

async def read_todos(request: Request, db: Session = Depends(get_db)):

    todos = crud.get_todos(db)

    tags = crud.get_tags(db)

    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos, "tags": tags})



@app.post("/todos/", response_class=RedirectResponse)

async def create_todo(request: Request, title: str = Form(...), tag_id: Optional[int] = Form(None), db: Session = Depends(get_db)):

    if tag_id:

        tag = crud.get_tag_by_id(db, tag_id=tag_id)

        if not tag:

            raise HTTPException(status_code=404, detail="Tag not found. Please add the tag first.")

    todo = schemas.TodoCreate(title=title, completed=False)

    crud.create_todo_with_tag(db=db, todo=todo, tag_id=tag_id)

    return RedirectResponse(url="/", status_code=303)



@app.delete("/todos/{todo_id}", response_class=RedirectResponse)

async def delete_todo(todo_id: int, db: Session = Depends(get_db)):

    crud.delete_todo(db=db, todo_id=todo_id)

    return RedirectResponse(url="/", status_code=303)



@app.put("/todos/{todo_id}", response_class=RedirectResponse)

async def edit_todo(todo_id: int, todo_data: schemas.TodoEdit, db: Session = Depends(get_db)):

    todo = crud.update_todo_title(db=db, todo_id=todo_id, title=todo_data.title)

    if not todo:

        raise HTTPException(status_code=404, detail="Todo not found")

    return RedirectResponse(url="/", status_code=303)



@app.post("/todos/{todo_id}/complete", response_class=RedirectResponse)

async def toggle_complete(todo_id: int, db: Session = Depends(get_db)):

    todo = crud.toggle_complete(db=db, todo_id=todo_id)

    if not todo:

        raise HTTPException(status_code=404, detail="Todo not found")

    return RedirectResponse(url="/", status_code=303)



# Tag routes

@app.post("/tags/", response_class=RedirectResponse)

async def create_tag(request: Request, name: str = Form(...), db: Session = Depends(get_db)):

    tag = schemas.TagCreate(name=name)

    crud.create_tag(db=db, tag=tag)

    return RedirectResponse(url="/", status_code=303)



@app.delete("/tags/{tag_id}", response_class=RedirectResponse)

async def delete_tag(tag_id: int, db: Session = Depends(get_db)):

    crud.delete_tag(db=db, tag_id=tag_id)

    return RedirectResponse(url="/", status_code=303)

