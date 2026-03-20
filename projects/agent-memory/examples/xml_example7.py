"""
Memory xml_example7
xml_example7
"""
import xml.etree.ElementTree as ET


def demo():
    tree = ET.parse("/dev/stdin")
    print(tree.getroot())


if __name__ == "__main__":
    demo()
