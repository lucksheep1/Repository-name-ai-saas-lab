"""
Memory CSV Reader
CSV reader
"""
from memory import Memory
import csv


def demo():
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["col1", "col2"])
        writer.writerow(["a", "b"])
    
    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)


if __name__ == "__main__":
    demo()
