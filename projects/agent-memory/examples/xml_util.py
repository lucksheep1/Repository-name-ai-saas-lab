"""
Memory xml
xml utilities
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("root")
    ET.SubElement(root, "child").text = "text"
    print(ET.tostring(root))


if __name__ == "__main__":
    demo()
