"""
Memory csv_example3
csv_example3
"""
import csv


def demo():
    import io
    data = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    print(output.getvalue())


if __name__ == "__main__":
    demo()
