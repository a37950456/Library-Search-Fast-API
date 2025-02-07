from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="Library Management API",
    description="A RESTful API service for managing a library catalog system",
    version="1.0.0"
)

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    isbn: str
    published_year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Simulate a database with a list
books_db = []

@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message"""
    return {"message": "Welcome to the Library Management API"}

@app.get("/books", response_model=List[Book])
def list_books(skip: int = 0, limit: int = 10):
    """
    Retrieve a list of books with pagination support
    """
    return books_db[skip : skip + limit]

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """
    Retrieve a specific book by its ID
    """
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

@app.post("/books", response_model=Book, status_code=201)
def create_book(book: BookCreate):
    """
    Create a new book entry
    """
    book_dict = book.dict()
    book_dict.update({
        "id": len(books_db),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    book_entry = Book(**book_dict)
    books_db.append(book_entry)
    return book_entry

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate):
    """
    Update an existing book's details
    """
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_dict = book.dict()
    book_dict.update({
        "id": book_id,
        "created_at": books_db[book_id].created_at,
        "updated_at": datetime.now()
    })
    books_db[book_id] = Book(**book_dict)
    return books_db[book_id]

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """
    Delete a book by its ID
    """
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    
    books_db.pop(book_id)
    return {"message": f"Book with id {book_id} has been deleted"}

# Example usage to add some initial data
@app.on_event("startup")
async def startup_event():
    # Add some sample books
    sample_books = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "description": "A story of the fabulously wealthy Jay Gatsby",
            "isbn": "978-0743273565",
            "published_year": 1925
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "description": "The story of racial injustice and loss of innocence",
            "isbn": "978-0446310789",
            "published_year": 1960
        }
    ]
    
    for book in sample_books:
        create_book(BookCreate(**book))