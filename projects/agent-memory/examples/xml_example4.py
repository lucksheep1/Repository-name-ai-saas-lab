"""
Memory xml_example4
xml_example4
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("data")
    items = ET.SubElement(root, "items")
    item = ET.SubElement(items, "item", name="test")
    item.text = "value"
    print(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    demo()
