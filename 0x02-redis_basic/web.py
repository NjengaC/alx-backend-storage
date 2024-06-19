#!/usr/bin/env python3

"""This module implement a cache storage for web"""
import redis
import requests
from functools import wraps
from typing import Callable
import time


def track_url(func: Callable) -> Callable:
    """Track url of a web app"""

    def track(*args: str) -> str:
        """Track url now"""
        key: str = f"count:{args[0]}"
        r = redis.Redis()
        r.incr(key)
        r.setex(args[0], 10, 'cached_data')
        r.expire(key, 10)
        result = func(args[0])
        return result
    return track


@track_url
def get_page(url: str) -> str:
    """get a page from a website"""
    resp = requests.get(url)
    return str(resp.text)


if __name__ == '__main__':
    r = redis.Redis()
    get_page('http://slowwly.robertomurray.co.uk')
    get_page('http://slowwly.robertomurray.co.uk')
    get_page('http://slowwly.robertomurray.co.uk')
    print(r.get('count:http://slowwly.robertomurray.co.uk'))
    time.sleep(12)
    get_page('http://slowwly.robertomurray.co.uk')
    print(r.get('count:http://slowwly.robertomurray.co.uk'))
