"""
Memory xml_example10
xml_example10
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("data")
    item = ET.SubElement(root, "item", id="1")
    item.text = "content"
    print(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    demo()
