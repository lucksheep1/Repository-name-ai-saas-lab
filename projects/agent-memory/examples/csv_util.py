"""
Memory csv
csv utilities
"""
import csv


def demo():
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["a", "b"])
    print(output.getvalue())


if __name__ == "__main__":
    demo()
