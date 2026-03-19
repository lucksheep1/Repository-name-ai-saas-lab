"""
Memory xml_example2
xml_example2
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("root")
    child = ET.SubElement(root, "child")
    child.text = "hello"
    print(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    demo()
