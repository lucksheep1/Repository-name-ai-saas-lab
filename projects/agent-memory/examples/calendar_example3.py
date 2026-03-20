"""
Memory calendar_example3
calendar_example3
"""
import calendar


def demo():
    c = calendar.Calendar()
    for d in c.itermonthdays(2024, 1):
        if d != 0:
            print(d, end=" ")
    print()


if __name__ == "__main__":
    demo()
