import pytest
from fastapi.testclient import TestClient
from main import app, RateLimiter, books_db, BookCreate, Book

# Create a new FastAPI app instance for testing without rate limiting
@pytest.fixture
def test_app():
    app.dependency_overrides[RateLimiter] = lambda: RateLimiter(requests_per_minute=100)  # Set a high limit for testing
    yield app
    app.dependency_overrides.clear()

# Initialize the test client with the test app
@pytest.fixture
def client(test_app):
    return TestClient(test_app)

# Test RateLimiter
@pytest.fixture
def rate_limiter():
    return RateLimiter(requests_per_minute=2)

@pytest.mark.asyncio
async def test_rate_limiter(rate_limiter):
    # Simulate requests from the same client
    class MockRequest:
        class Client:
            @property
            def host(self):
                return "127.0.0.1"

        def __init__(self):
            self.client = self.Client()

    request = MockRequest()

    # Allow 2 requests
    assert await rate_limiter(request)
    assert await rate_limiter(request)

    # Third request should raise HTTPException
    with pytest.raises(Exception) as excinfo:
        await rate_limiter(request)
    assert excinfo.value.status_code == 429

# Reset the rate limiter before each book endpoint test
@pytest.fixture(autouse=True)
def reset_rate_limiter():
    rate_limiter_instance = RateLimiter(requests_per_minute=2)
    yield
    rate_limiter_instance.reset()  # Reset the rate limiter after each test

# Test book endpoints
def test_create_book(client):
    response = client.post("/books", json={
        "title": "New Book",
        "author": "Author Name",
        "description": "A new book description",
        "isbn": "123-4567890123",
        "published_year": 2023
    })
    assert response.status_code == 201
    assert response.json()["title"] == "New Book"

def test_list_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book(client):
    response = client.get("/books/0")
    assert response.status_code == 200
    assert "title" in response.json()

def test_update_book(client):
    response = client.put("/books/0", json={
        "title": "Updated Book",
        "author": "Updated Author",
        "description": "Updated description",
        "isbn": "123-4567890123",
        "published_year": 2023
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"

def test_delete_book(client):
    response = client.delete("/books/0")
    assert response.status_code == 200
    assert response.json()["message"] == "Book with id 0 has been deleted"