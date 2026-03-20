"""
Memory xml_example12
xml_example12
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("root")
    child = ET.SubElement(root, "child")
    child.text = "text"
    print(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    demo()
