"""
Memory csv_example9
csv_example9
"""
import csv


def demo():
    import io
    data = "name,age\nAlice,30\nBob,25"
    reader = csv.DictReader(io.StringIO(data))
    for row in reader:
        print(row["name"])


if __name__ == "__main__":
    demo()
