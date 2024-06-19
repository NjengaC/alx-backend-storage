import requests
import redis
import functools

# Connect to the local Redis server
r = redis.Redis(host='localhost', port=6379, db=0)


def cache_with_expiration(expiration: int):
    def decorator_get_page(func):
        @functools.wraps(func)
        def wrapper_get_page(url):
            # Check if the URL content is cached
            cached_content = r.get(url)

            if cached_content:
                r.incr(f"count:{url}")
                return cached_content.decode('utf-8')
            else:
                # If content is not cached, fetch the content from the URL
                content = func(url)

                # Cache the content with an expiration time
                r.setex(url, expiration, content)

                # Initialize the access count to 1
                r.set(f"count:{url}", 1)

                return content
        return wrapper_get_page
    return decorator_get_page


@cache_with_expiration(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
