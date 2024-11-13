from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, Todo as TodoSchema

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[TodoSchema])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of todos.
    
    Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    
    Returns:
    - List of todo items
    """
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return todos

@router.post("/", response_model=TodoSchema)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo item.
    
    Parameters:
    - todo: Todo item to create (title, description, etc.)
    
    Returns:
    - Created todo item
    """
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/{todo_id}", response_model=TodoSchema)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific todo by ID.
    
    Parameters:
    - todo_id: ID of the todo to retrieve
    
    Returns:
    - Todo item
    
    Raises:
    - 404: Todo not found
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    """
    Update a specific todo by ID.
    
    Parameters:
    - todo_id: ID of the todo to update
    - todo: Updated todo data
    
    Returns:
    - Updated todo item
    
    Raises:
    - 404: Todo not found
    """
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific todo by ID.
    
    Parameters:
    - todo_id: ID of the todo to delete
    
    Returns:
    - Message confirming deletion
    
    Raises:
    - 404: Todo not found
    """
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}