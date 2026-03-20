"""
Memory csv_example7
csv_example7
"""
import csv


def demo():
    import io
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": "30"})
    print(output.getvalue())


if __name__ == "__main__":
    demo()
