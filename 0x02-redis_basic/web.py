#!/usr/bin/env python3

"""This module implements a cache storage for web pages."""
import redis
import requests
from functools import wraps
from typing import Callable
import time

# Initialize Redis connection
r = redis.Redis()


def track_url(func: Callable) -> Callable:
    """Track URL accesses and cache the result with expiration."""

    @wraps(func)
    def wrapper(url: str) -> str:
        """Track URL and cache the result."""
        count_key = f"count:{url}"
        cached_content = r.get(url)

        if cached_content:
            r.incr(count_key)
            return cached_content.decode('utf-8')

        r.incr(count_key)
        result = func(url)
        r.setex(url, 10, result)
        r.expire(count_key, 10)
        return result

    return wrapper


@track_url
def get_page(url: str) -> str:
    """Get a page from a website."""
    resp = requests.get(url)
    return resp.text


if __name__ == '__main__':
    ur = 'http://slowwly.robertomurray.co.uk/'
    rl = 'delay/5000/url/http://www.google.co.uk'
    url = ur + rl
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))
    print(f"Access count: {r.get(f'count:{url}').decode('utf-8')}")
    time.sleep(12)
    print(get_page(url))
    print(f"Access count: {r.get(f'count:{url}').decode('utf-8')}")
