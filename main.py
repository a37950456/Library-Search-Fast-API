from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta

# rate limiter
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

app = FastAPI(
    title="Library Management API",
    description="A RESTful API service for managing a library catalog system",
    version="1.0.0"
)

# book class
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


# Rate limiter
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[datetime]] = {}

    async def __call__(self, request: Request):
        client_ip = request.client.host
        now = datetime.now()
        
        # Initialize or clean old requests for this IP
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Remove requests older than 1 minute
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < timedelta(minutes=1)
        ]
        
        # Check if rate limit is exceeded
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again in a minute."
            )
        
        # Add current request
        self.requests[client_ip].append(now)
        return True

# Simulate a database with a list
books_db = []
# create rate limiter
rate_limiter = RateLimiter(requests_per_minute=60)

@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message"""
    return {"message": "Welcome to the Library Management API"}

@app.get("/books", response_model=List[Book])
async def list_books(
    skip: int = 0, 
    limit: int = 10,
    _: bool = Depends(rate_limiter)
):
    """
    Retrieve a list of books with pagination support
    """
    return books_db[skip : skip + limit]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(
    book_id: int,
    _: bool = Depends(rate_limiter)
):
    """
    Retrieve a specific book by its ID
    """
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

@app.post("/books", response_model=Book, status_code=201)
async def create_book(
    book: BookCreate,
    _: bool = Depends(rate_limiter)
):
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
async def update_book(
    book_id: int, 
    book: BookCreate,
    _: bool = Depends(rate_limiter)
):
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
async def delete_book(
    book_id: int,
    _: bool = Depends(rate_limiter)
):
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