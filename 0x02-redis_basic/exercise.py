#!/usr/bin/env python3
"""
Redis
"""


import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Method counter
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap
        """

        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Call history method
    """

    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap
        """

        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


def replay(redis_client, method):
    """
    Display the history of calls.
    """

    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    inputs = redis_client.lrange(i, 0, -1)
    outputs = redis_client.lrange(o, 0, -1)

    call_history = list(zip(inputs, outputs))

    return call_history


class Cache:
    """
    Cacheclass
    """

    def __init__(self):
        """
        Initialize redis
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Generate a random key and store
        """

        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> UnionOfTypes:
        """
        Convert the data back
        to its normal type
        """

        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """Get a number"""

        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """Get a string"""

        return self.decode("utf-8")
