from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Book Models
class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    isbn: str
    published_year: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A story of the fabulously wealthy Jay Gatsby",
                "isbn": "978-0743273565",
                "published_year": 1925
            }
        }
    }

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

# Rate Limiter
class RateLimiter:
    def __init__(self, requests_per_minute: int = 2):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[datetime]] = {}
        self.lock = asyncio.Lock()  # Ensure thread safety
        logger.info(f"Initialized RateLimiter with limit: {requests_per_minute}")

    def reset(self):
        """Reset the rate limiter state"""
        logger.info("Resetting rate limiter")
        self.requests.clear()

    async def __call__(self, request: Request) -> bool:
        client_ip = request.client.host  # Get real client IP
        now = datetime.now()

        async with self.lock:  # Ensure thread safety
            logger.info(f"Processing request from {client_ip} at {now}")

            # Initialize requests list for this client
            if client_ip not in self.requests:
                self.requests[client_ip] = []
                logger.info(f"Initialized request tracking for {client_ip}")

            # Clean old requests
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if (now - req_time) < timedelta(minutes=1)
            ]

            # Check if the limit is exceeded
            current_count = len(self.requests[client_ip])
            logger.info(f"Current request count for {client_ip}: {current_count}")

            if current_count >= self.requests_per_minute:
                logger.warning(f"Rate limit exceeded for {client_ip}")
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again in a minute."
                )

            # Add the current request
            self.requests[client_ip].append(now)
            logger.info(f"Added request for {client_ip}. New count: {len(self.requests[client_ip])}")
        
        return True

# Create rate limiter instance with a low limit for testing
rate_limiter = RateLimiter(requests_per_minute=2)

def get_rate_limiter() -> RateLimiter:
    """Get the rate limiter instance"""
    return rate_limiter

# Initialize database
books_db: List[Book] = []

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Add sample data
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
        book_dict = book.copy()
        book_dict.update({
            "id": len(books_db),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
        books_db.append(Book(**book_dict))
    
    yield
    
    # Cleanup
    books_db.clear()

# Initialize FastAPI
app = FastAPI(
    title="Library Management API",
    description="A RESTful API service for managing a library catalog system",
    version="1.0.0",
    lifespan=lifespan
)

# Endpoints
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Library Management API :)"}

@app.get("/books", response_model=List[Book])
async def list_books(
    skip: int = 0, 
    limit: int = 10,
    _: bool = Depends(rate_limiter)  # Fixed dependency
):
    return books_db[skip : skip + limit]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(
    book_id: int,
    _: bool = Depends(rate_limiter)
):
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

@app.post("/books", response_model=Book, status_code=201)
async def create_book(
    book: BookCreate,
    _: bool = Depends(rate_limiter)
):
    book_dict = book.model_dump()
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
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_dict = book.model_dump()
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
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    
    books_db.pop(book_id)
    return {"message": f"Book with id {book_id} has been deleted"}