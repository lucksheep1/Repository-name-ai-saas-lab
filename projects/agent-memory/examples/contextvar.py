"""
Memory ContextVar
Context variables
"""
from memory import Memory
from contextvars import ContextVar


request_id: ContextVar[str] = ContextVar("request_id")


def set_request_id(req_id: str):
    request_id.set(req_id)


def get_request_id() -> str:
    return request_id.get("default")


def demo():
    set_request_id("123")
    print(get_request_id())


if __name__ == "__main__":
    demo()
