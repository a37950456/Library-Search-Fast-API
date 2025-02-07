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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.