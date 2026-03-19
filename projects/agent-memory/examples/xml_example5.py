"""
Memory xml_example5
xml_example5
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("root")
    ET.SubElement(root, "child", attrib={"id": "1"})
    print(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    demo()
