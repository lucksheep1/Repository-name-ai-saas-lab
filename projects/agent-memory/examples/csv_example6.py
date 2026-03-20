"""
Memory csv_example6
csv_example6
"""
import csv


def demo():
    import io
    data = "name,value\ntest,100"
    writer = csv.writer(io.StringIO())
    writer.writerow(["name", "value"])
    writer.writerow(["test", "100"])
    print("written")


if __name__ == "__main__":
    demo()
