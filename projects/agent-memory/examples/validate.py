"""
Memory Validate
Validation decorator
"""
from memory import Memory


def validate(**validators):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for name, validator in validators.items():
                if name in kwargs:
                    if not validator(kwargs[name]):
                        raise ValueError(f"Invalid {name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@validate(x=lambda x: x > 0)
def positive(x):
    return x


def demo():
    print(positive(5))


if __name__ == "__main__":
    demo()
