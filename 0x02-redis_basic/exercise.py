#!/usr/bin/env python3
"""This module contains the class Cache
used to interact with a Redis database
"""

import redis
import uuid
from typing import Union


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
