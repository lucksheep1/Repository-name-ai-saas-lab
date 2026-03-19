"""
Memory XML
XML parsing
"""
from memory import Memory
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("root")
    child = ET.SubElement(root, "child")
    child.text = "text"
    
    tree = ET.ElementTree(root)
    tree.write("test.xml")
    print("XML written")


if __name__ == "__main__":
    demo()
