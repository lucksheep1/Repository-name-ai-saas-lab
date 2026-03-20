"""
Memory csv_example10
csv_example10
"""
import csv


def demo():
    import io
    data = "name,age\nAlice,30\nBob,25"
    reader = csv.reader(io.StringIO(data))
    for row in reader:
        print(row)


if __name__ == "__main__":
    demo()
