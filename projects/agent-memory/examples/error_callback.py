"""
Memory Error Callback
Error callback
"""
from memory import Memory


async def on_error(ws, error):
    print(f"Error: {error}")


def demo():
    print("Error handler ready")


if __name__ == "__main__":
    demo()
