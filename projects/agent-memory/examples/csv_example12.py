"""
Memory csv_example12
csv_example12
"""
import csv


def demo():
    import io
    data = "a,b\n1,2\n3,4"
    reader = csv.reader(io.StringIO(data))
    for row in reader:
        print(row)


if __name__ == "__main__":
    demo()
