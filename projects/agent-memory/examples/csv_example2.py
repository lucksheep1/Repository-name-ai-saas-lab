"""
Memory csv_example2
csv_example2
"""
import csv


def demo():
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["a", "b", "c"])
    print(output.getvalue())


if __name__ == "__main__":
    demo()
