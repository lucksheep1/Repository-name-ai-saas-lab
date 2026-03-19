"""
Memory Validator
Validate memory data
"""
from memory import Memory


class Validator:
    @staticmethod
    def validate_content(content: str) -> tuple:
        if not content:
            return False, "Empty content"
        if len(content) > 10000:
            return False, "Content too long"
        return True, None
    
    @staticmethod
    def validate_tags(tags: list) -> tuple:
        if not tags:
            return True, None
        if len(tags) > 20:
            return False, "Too many tags"
        return True, None


def demo():
    print(f"Valid: {Validator.validate_content('Test')}")
    print(f"Valid: {Validator.validate_tags(['a', 'b'])}")


if __name__ == "__main__":
    demo()
