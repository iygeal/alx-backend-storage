#!/usr/bin/env python3
"""This module contains the class Cache
used to interact with a Redis database
"""

import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """Cache class for storing and retrieving data from Redis
    """

    def __init__(self):
        """Initialize the Cache instance with a Redis client
        and flush the Redis database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return a unique key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[
            Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """Retrieves data from Redis and optionally converts it using fn

        Args:
            key (str): The key to retrieve the data for
            fn (Optional[ Callable], optional): Function to convert the data.
            Defaults to None.

        Returns:
            Optional[Union[str, bytes, int, float]]: Retrieved data or None
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve data from Redis and convert it to a UTF-8 string

        Args:
            key (str): The key to retrieve the data for

        Returns:
            Optional[str]: Retrieved data as a string or None
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieves data from Redis and converts it to an integer

        Args:
            key (str): The key to retrieve the data for

        Returns:
            Optional[int]: The retrieved data as an integer or None
        """
        value = self.get(key)
        if value is None:
            return None
        try:
            value = int(value)
        except Exception:
            value = 0
        return value
