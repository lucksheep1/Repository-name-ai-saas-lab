"""
Memory email
email utilities
"""
import email


def demo():
    msg = email.message.EmailMessage()
    msg["Subject"] = "Test"
    print(msg)


if __name__ == "__main__":
    demo()
