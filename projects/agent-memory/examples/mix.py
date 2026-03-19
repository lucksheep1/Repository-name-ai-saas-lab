"""
Memory Mix
Mix classes
"""
from memory import Memory


class Mix:
    @staticmethod
    def create(storage="json"):
        return Memory(storage=storage, path=f"./{storage}.json")


def demo():
    print(Mix.create())


if __name__ == "__main__":
    demo()
