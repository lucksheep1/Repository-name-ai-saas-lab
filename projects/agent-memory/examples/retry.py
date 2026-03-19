"""
Memory Retry
Retry decorator
"""
from memory import Memory


def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if _ < max_attempts - 1:
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator


@retry(3)
def failing_func():
    raise Exception("Fail")


def demo():
    print("Retry ready")


if __name__ == "__main__":
    demo()
