import hashlib
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .models import User, Book
from .schemas import UserCreate, BookCreate



# Password hashing context (create once)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        hashed_password=user.password  # ❌ no hashing now
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# -------------------- BOOK CRUD --------------------

def create_book(db: Session, book: BookCreate, user_id: int):
    db_book = Book(
        **book.dict(),   # data from request body
        owner_id=user_id # controlled by backend
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session):
    return db.query(Book).all()


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if book is None:
        return None

    db.delete(book)
    db.commit()
    return book
