"""
Rate limiting middleware for the AI Agent Platform
Implements FR-012: System MUST implement basic rate limiting with retry mechanisms to manage API costs and prevent abuse
"""
import asyncio
import time
from collections import defaultdict, deque
from typing import Dict
from ..db.settings import settings
from ..utils.logging import Logger


class RateLimiter:
    """
    In-memory rate limiter implementation
    Tracks requests per user and enforces limits
    """

    def __init__(self):
        # Store request timestamps for each user
        self.requests = defaultdict(deque)
        # Lock for thread safety (though in async context, we'll handle differently)
        self._lock = asyncio.Lock()

    async def is_allowed(self, user_id: str) -> tuple[bool, float]:
        """
        Check if a request from the given user is allowed

        Args:
            user_id: ID of the user making the request

        Returns:
            tuple[bool, float]: (is_allowed, time_until_reset_in_seconds)
        """
        async with self._lock:
            now = time.time()
            window_start = now - settings.rate_limit_window

            # Clean old requests outside the window
            user_requests = self.requests[user_id]
            while user_requests and user_requests[0] < window_start:
                user_requests.popleft()

            # Check if the user is within the rate limit
            current_count = len(user_requests)

            if current_count < settings.rate_limit_requests:
                # Add the current request
                user_requests.append(now)
                return True, 0.0

            # Calculate time until oldest request expires
            oldest_request = user_requests[0] if user_requests else now
            time_until_reset = oldest_request + settings.rate_limit_window - now

            return False, max(0.0, time_until_reset)

    async def get_remaining_requests(self, user_id: str) -> tuple[int, float]:
        """
        Get the number of remaining requests and time until reset

        Args:
            user_id: ID of the user

        Returns:
            tuple[int, float]: (remaining_requests, time_until_reset_in_seconds)
        """
        async with self._lock:
            now = time.time()
            window_start = now - settings.rate_limit_window

            # Clean old requests
            user_requests = self.requests[user_id]
            while user_requests and user_requests[0] < window_start:
                user_requests.popleft()

            remaining = settings.rate_limit_requests - len(user_requests)
            oldest_request = user_requests[0] if user_requests else now
            time_until_reset = oldest_request + settings.rate_limit_window - now

            return max(0, remaining), max(0.0, time_until_reset)


# Global rate limiter instance
rate_limiter = RateLimiter()


async def check_rate_limit(user_id: str) -> bool:
    """
    Check if a user is within their rate limit

    Args:
        user_id: ID of the user making the request

    Returns:
        bool: True if allowed, raises exception if rate limited
    """
    is_allowed, time_until_reset = await rate_limiter.is_allowed(user_id)

    if not is_allowed:
        Logger.warning(f"Rate limit exceeded for user: {user_id}", extra={
            "time_until_reset": time_until_reset
        })

        # Raise an exception that can be caught by the API framework
        from fastapi import HTTPException
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Please try again in {time_until_reset:.1f} seconds.",
                "retry_after": time_until_reset
            }
        )

    return True


async def get_rate_limit_status(user_id: str) -> Dict[str, int]:
    """
    Get the current rate limit status for a user

    Args:
        user_id: ID of the user

    Returns:
        Dict[str, int]: Rate limit status information
    """
    remaining, time_until_reset = await rate_limiter.get_remaining_requests(user_id)

    return {
        "limit": settings.rate_limit_requests,
        "remaining": remaining,
        "reset_time": time.time() + time_until_reset,
        "window_size": settings.rate_limit_window
    }


class RateLimitMiddleware:
    """
    FastAPI middleware for rate limiting
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # Extract user ID from request (this is simplified; in practice you'd extract from auth)
        # For now, we'll use a mock user ID or IP address
        user_id = "anonymous"  # This would be replaced with actual user ID from auth

        # Check rate limit
        try:
            await check_rate_limit(user_id)
        except Exception as e:
            # Send rate limit error response
            response_headers = [
                (b"x-ratelimit-limit", str(settings.rate_limit_requests).encode()),
                (b"x-ratelimit-remaining", b"0"),
                (b"x-ratelimit-reset", str(int(time.time() + 60)).encode()),  # Fixed 60s reset for error case
            ]

            await send({
                "type": "http.response.start",
                "status": 429,
                "headers": response_headers,
            })
            await send({
                "type": "http.response.body",
                "body": b'{"detail":"Rate limit exceeded"}',
                "more_body": False,
            })
            return

        # Add rate limit headers to successful responses
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Get rate limit status to add headers
                status = await get_rate_limit_status(user_id)

                # Add rate limit headers
                rate_limit_headers = [
                    (b"x-ratelimit-limit", str(status["limit"]).encode()),
                    (b"x-ratelimit-remaining", str(status["remaining"]).encode()),
                    (b"x-ratelimit-reset", str(int(status["reset_time"])).encode()),
                ]

                # Add existing headers
                headers = message.get("headers", [])
                headers.extend(rate_limit_headers)
                message["headers"] = headers

            await send(message)

        await self.app(scope, receive, send_wrapper)


# Utility function to reset rate limits for a user (useful for testing)
async def reset_rate_limit(user_id: str):
    """
    Reset rate limit for a specific user (mainly for testing purposes)

    Args:
        user_id: ID of the user to reset
    """
    async with rate_limiter._lock:
        if user_id in rate_limiter.requests:
            del rate_limiter.requests[user_id]