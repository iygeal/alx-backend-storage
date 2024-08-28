import redis
import requests
from typing import Callable, Union
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def cache_page(method: Callable, cache_expiration: int = 10) -> Callable:
    """Decorator to cache the result of a function call with a specified expiration time.

    Args:
        method (Callable): The function to be decorated.
        cache_expiration (int, optional): The cache expiration time in seconds. Defaults to 10.

    Returns:
        Callable: The decorated function.
    """

    @wraps(method)
    def wrapper(url: str, *args, **kwargs) -> Union[str, None]:
        """Wrapper function that checks if the response is in the cache,
        if so return it, otherwise call the actual function to fetch the data,
        cache the response with the specified expiration time, and
        increment the count for the URL access.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            Union[str, None]: The HTML content of the URL, or None if an error occurs.
        """

        cache_key = f"cache:{url}"
        count_key = f"count:{url}"

        try:
            # Check if the response is in the cache
            cached_response = redis_client.get(cache_key)
            if cached_response:
                redis_client.incr(count_key)
                return cached_response.decode('utf-8')

            # Call the actual function to fetch the data
            response = method(url, *args, **kwargs)

            # Cache the response with the specified expiration time
            redis_client.setex(cache_key, cache_expiration, response)

            # Increment the count for the URL access
            redis_client.incr(count_key)

            return response
        except (requests.RequestException, redis.exceptions.RedisError) as e:
            # Handle network errors and Redis exceptions
            print(f"Error: {e}")
            return None

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-2xx status codes
    return response.text
