from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Engine, text

from . import crud
from . import schemas
from .database import Base, engine, get_db


app = FastAPI()

Base.metadata.create_all(bind=engine)

# -------------------- ROOT --------------------

@app.get("/")
async def root():
    return {"message": "Hello World"}


# -------------------- HEALTH CHECK --------------------

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "UP",
            "database": "PostgreSQL",
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "DOWN",
            "database": "PostgreSQL",
            "error": str(e)
        }


# -------------------- USER APIs --------------------

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------------------- BOOK APIs --------------------

@app.post("/users/{user_id}/books", response_model=schemas.BookResponse)
def create_book(
    user_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_book(db, book, user_id)


@app.get("/books", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.delete_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}



