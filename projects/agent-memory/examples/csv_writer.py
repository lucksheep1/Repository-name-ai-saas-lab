"""
Memory CSV Writer
CSV writer
"""
from memory import Memory
import csv


def demo():
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["col1", "col2"])
        writer.writerow(["a", "b"])
    print("Written")


if __name__ == "__main__":
    demo()
