"""
Memory xml_example8
xml_example8
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("root")
    ET.SubElement(root, "child", attrib={"id": "1"})
    print(ET.tostring(root))


if __name__ == "__main__":
    demo()
