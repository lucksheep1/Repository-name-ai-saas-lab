"""
Memory xml_example13
xml_example13
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("root")
    ET.SubElement(root, "child", attrib={"name": "value"})
    print(ET.tostring(root))


if __name__ == "__main__":
    demo()
