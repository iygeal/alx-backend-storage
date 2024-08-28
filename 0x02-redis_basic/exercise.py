#!/usr/bin/env python3
"""This module contains the class Cache
used to interact with a Redis database
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def replay(method: Callable):
    """Display the history of calls of a particular function"""
    redis_instance = method.__self__._redis
    # Get the method's qualified name
    method_name = method.__qualname__
    # Retrieve inputs and outputs from Redis
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)

    # print the number of times the method was called
    print(f"{method_name} was called {len(inputs)} times:")

    # Loop over inputs and outputs
    for input_data, output_data in zip(inputs, outputs):
        input_data = input_data.decode("utf-8")
        output_data = output_data.decode("utf-8")
        # Print the input and output
        print(f"{method_name}(*{input_data}) -> {output_data}")


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs and outputs for a function
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Decorator function that stores the history of inputs and outputs"""
        # Define the keys for storing inputs and outputs
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Store the input arguments in the inputs list
        self._redis.rpush(inputs_key, str(args))

        # Execute the original method and capture its output
        result = method(self, *args, **kwargs)

        # Store the output in the outputs list
        self._redis.rpush(outputs_key, str(result))

        # Return the output
        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times
    a method is called
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments the call count in Redis"""
        # Get the method's qualified name as the key
        key = method.__qualname__
        # Increment the count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache class for storing and retrieving data from Redis
    """

    def __init__(self):
        """Initialize the Cache instance with a Redis client
        and flush the Redis database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
            fn (Optional[Callable], optional): Function to convert the data.
            Defaults to None.

        Returns:
            Optional[Union[str, bytes, int, float]]: Retrieved data or None
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

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
        return self.get(key, fn=int)
