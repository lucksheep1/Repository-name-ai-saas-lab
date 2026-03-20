"""
Memory xml_example11
xml_example11
"""
import xml.etree.ElementTree as ET


def demo():
    tree = ET.parse("/etc/hosts")
    root = tree.getroot()
    print(root.tag)


if __name__ == "__main__":
    demo()
