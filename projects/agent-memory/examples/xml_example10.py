"""
Memory xml_example10
xml_example10
"""
import xml.etree.ElementTree as ET


def demo():
    root = ET.Element("config")
    setting = ET.SubElement(root, "setting", name="debug")
    setting.text = "true"
    print(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    demo()
