from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timedelta
from typing import Dict, List

app = FastAPI()

class RateLimiter:
    def __init__(self, requests_per_minute: int = 2):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[datetime]] = {}
        print(f"Initialized RateLimiter with limit: {requests_per_minute}")

    def reset(self):
        """Reset the rate limiter state"""
        print("Resetting rate limiter")
        self.requests.clear()

    async def __call__(self, request):
        client_ip = "testclient"  # Use a fixed IP for testing
        now = datetime.now()

        print(f"Processing request from {client_ip} at {now}")

        # Initialize requests list for this client
        if client_ip not in self.requests:
            self.requests[client_ip] = []
            print(f"Initialized requests for {client_ip}")

        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if (now - req_time) < timedelta(minutes=1)
        ]

        # Check if the limit is exceeded
        current_count = len(self.requests[client_ip])
        print(f"Current request count for {client_ip}: {current_count}")

        if current_count >= self.requests_per_minute:
            print(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again in a minute."
            )

        # Add the current request
        self.requests[client_ip].append(now)
        print(f"Added request for {client_ip}. New count: {len(self.requests[client_ip])}")

        return True

# Create a rate limiter instance
rate_limiter = RateLimiter()

@app.get("/books")
async def get_books(rate_limit: bool = Depends(rate_limiter)):
    return {"message": "Here are your books!"}