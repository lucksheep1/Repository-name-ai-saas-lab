"""
Memory xml_example
xml_example
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("root")
    print(ET.tostring(root))


if __name__ == "__main__":
    demo()
