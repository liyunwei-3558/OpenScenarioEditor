import xml.etree.ElementTree as ET


def change_one_xml(xml_path, xml_dw, update_content):
    # 打开xml文档
    doc = ET.parse(xml_path)
    root = doc.getroot()
    # 查找修改路劲
    sub1 = root.find(xml_dw)
    # 修改标签内容
    sub1.text = update_content
    # 保存修改
    doc.write(xml_path)

