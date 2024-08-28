#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """ Decorator counting how many times
    a URL is accessed """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper function that checks if a cached version of the page
        exists in Redis, and if so, returns it. Otherwise, it calls the
        wrapped method, stores the result in Redis and returns it.

        Also, it increments the count of times the page has been accessed
        in Redis.

        Args:
            url (str): The URL of the page to retrieve

        Returns:
            str: The HTML content of the page
        """
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    res = requests.get(url)
    return res.text
