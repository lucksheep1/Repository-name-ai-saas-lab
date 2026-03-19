"""
Memory CSV Dict Writer
CSV dict writer
"""
from memory import Memory
import csv


def demo():
    with open("data.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["col1", "col2"])
        writer.writeheader()
        writer.writerow({"col1": "a", "col2": "b"})
    print("Written")


if __name__ == "__main__":
    demo()
