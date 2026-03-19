"""
Memory csv_example4
csv_example4
"""
import csv


def demo():
    import io
    data = [["Name", "Age"], ["Alice", "30"]]
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerows(data)
    print(output.getvalue())


if __name__ == "__main__":
    demo()
