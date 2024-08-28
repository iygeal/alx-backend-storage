#!/usr/bin/env python3
"""This module contains a function to get HTML content of a URL
with caching and access tracking.
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client with default settings
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def cache_page(method: Callable[[str], str]) -> Callable[[str], str]:
    """Decorator to cache the result of a function call
    with an expiration time of 10 seconds."""

    @wraps(method)
    def wrapper(url: str, *args, **kwargs) -> str:
        """
        Wrapper function that checks if the response is in the cache,
        if so return it, otherwise call the actual function to fetch the data,
        cache the response with an expiration time of 10 seconds and
        increment the count for the URL access.

        Args:
            url (str): The URL to fetch data from

        Returns:
            str: The HTML content of the URL
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

            # Cache the response with an expiration time of 10 seconds
            redis_client.setex(cache_key, 10, response)

            # Increment the count for the URL access
            redis_client.incr(count_key)

            return response
        except redis.RedisError as e:
            # Handle Redis exceptions
            print(f"Redis error: {e}")
            return ""
        except requests.RequestException as e:
            # Handle HTTP request exceptions
            print(f"Request error: {e}")
            return ""

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        # Handle HTTP request exceptions
        print(f"Request error: {e}")
        return ""
