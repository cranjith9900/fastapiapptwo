from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# -------------------- BOOK SCHEMAS --------------------

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None   # ✅ typo fixed
    price: float


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------- USER SCHEMAS --------------------

class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=64)


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    books: List[BookResponse] = []   # ⚠️ see note below

    class Config:
        from_attributes = True
