"""
Memory CSV Dict Reader
CSV dict reader
"""
from memory import Memory
import csv


def demo():
    with open("data.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["col1", "col2"])
        writer.writeheader()
        writer.writerow({"col1": "a", "col2": "b"})
    
    with open("data.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)


if __name__ == "__main__":
    demo()
