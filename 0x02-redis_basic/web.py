#!/usr/bin/env python3
"""This module contains a function to get HTML content of a URL
with caching and access tracking.
"""
import requests
import redis
from functools import wraps

# Initialize Redis client
store = redis.Redis(host='localhost', port=6379, db=0)


def count_url_access(method):
    """Decorator counting how many times a URL is accessed
    and caching the result.
    """

    @wraps(method)
    def wrapper(url: str):
        """
        Wrapper function that checks if the response is in the cache,
        if so return it, otherwise call the actual function to fetch the data,
        cache the response with an expiration time of 10 seconds, and
        increment the count for the URL access.

        Args:
            url (str): The URL to fetch data from

        Returns:
            str: The HTML content of the URL
        """
        # Create cache and count keys for Redis
        cached_key = "cached:" + url
        count_key = "count:" + url

        # Check if the response is in the cache
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        # If not cached, fetch the page content
        html = method(url)

        # Increment the access count and cache the response
        # with an expiration time of 10 seconds
        store.incr(count_key)
        store.setex(cached_key, 10, html)

        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL."""
    res = requests.get(url)
    res.raise_for_status()  # Raise an exception for HTTP errors
    return res.text
