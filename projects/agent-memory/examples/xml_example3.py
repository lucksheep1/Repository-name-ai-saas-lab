"""
Memory xml_example3
xml_example3
"""
import xml.etree.ElementTree as ET


def demo():
    tree = ET.parse("/dev/null")
    print(tree.getroot())


if __name__ == "__main__":
    demo()
