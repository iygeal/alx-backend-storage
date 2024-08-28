import requests
from redis import Redis
from functools import wraps
from typing import Union

# Redis connection (modify host and port if necessary)
redis_client = Redis(host="localhost", port=6379)

# Cache expiration time in seconds
cache_expiration = 10


def cache_with_expiration(func):
    """Decorator to cache function results with expiration time in Redis.

    Args:
        func: The function to be decorated.

    Returns:
        A wrapper function that caches the result of the decorated function.
    """

    @wraps(func)
    def wrapper(url: str) -> Union[str, None]:
        cache_key = f"count:{url}"
        cached_content = redis_client.get(cache_key)

        if cached_content:
            # Increment counter and return cached content
            redis_client.incr(cache_key)
            return cached_content.decode("utf-8")

        # Fetch content if not cached, update cache, and return
        content = func(url)
        redis_client.set(cache_key, content, ex=cache_expiration)
        redis_client.incr(cache_key)
        return content

    return wrapper


@cache_with_expiration
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL using requests
    and tracks access count in Redis.

    Args:
        url: The URL to fetch content from.

    Returns:
        The HTML content of the URL as a string.
    """

    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-2xx status codes
    return response.content
