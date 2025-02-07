# Library Search FastAPI

A RESTful API service for managing a library catalog system built with FastAPI, SQLAlchemy, and Pydantic.

## Features

- Fast and efficient book search functionality
- CRUD operations for books and library management
- Data validation using Pydantic models
- SQLAlchemy ORM for database operations
- Interactive API documentation with Swagger UI

## Tech Stack

- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- Pydantic - Data validation using Python type annotations
- Uvicorn - Lightning-fast ASGI server
- SQLite - Lightweight database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Library-Search-Fast-API.git
cd Library-Search-Fast-API
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /books` - List all books
- `GET /books/{book_id}` - Get book details
- `POST /books` - Add a new book
- `PUT /books/{book_id}` - Update book details
- `DELETE /books/{book_id}` - Delete a book

## Using Swagger UI

After starting your server with `uvicorn main:app --reload`, you can access the interactive Swagger UI documentation at:
http://localhost:8000/docs

### How to Use Swagger UI

1. **Accessing the Documentation**
   - Open your browser and navigate to http://localhost:8000/docs
   - You'll see a fully interactive API documentation

2. **Testing Endpoints**
   - Each endpoint is listed with its HTTP method (GET, POST, PUT, DELETE)
   - Click on an endpoint to expand it and see details
   - Click the "Try it out" button to test the endpoint

3. **Example Operations**

   a. **Create a Book (POST /books)**
   - Click on POST /books
   - Click "Try it out"
   - Fill in the request body:
   ```json
   {
     "title": "The Hobbit",
     "author": "J.R.R. Tolkien",
     "description": "A fantasy novel about Bilbo Baggins",
     "isbn": "978-0547928227",
     "published_year": 1937
   }
   ```
   - Click "Execute"

   b. **List Books (GET /books)**
   - Click on GET /books
   - Click "Try it out"
   - Optionally adjust skip/limit parameters
   - Click "Execute"

   c. **Get Single Book (GET /books/{book_id})**
   - Click on GET /books/{book_id}
   - Click "Try it out"
   - Enter a book_id (e.g., 0)
   - Click "Execute"

   d. **Update Book (PUT /books/{book_id})**
   - Click on PUT /books/{book_id}
   - Click "Try it out"
   - Enter a book_id
   - Modify the request body
   - Click "Execute"

   e. **Delete Book (DELETE /books/{book_id})**
   - Click on DELETE /books/{book_id}
   - Click "Try it out"
   - Enter a book_id
   - Click "Execute"

4. **Response Information**
   - After executing a request, you'll see:
     - The curl command equivalent
     - The request URL
     - The response status code
     - The response body
     - Response headers

5. **Schema Information**
   - At the bottom of the page, you'll find detailed schema definitions
   - The Book schema shows all required and optional fields

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.