import json
from xml.etree.ElementTree import Element, SubElement, tostring, parse
from xml.dom import minidom

json_file_path = './public/codes'

def generateJSON():
    global json_file_path
    # 读取JSON文件
    with open(json_file_path+'.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 解析原始数据，并构造所需的格式
    result = []
    for item in data.get('data', []):
        code_value = item.get('code')
        if code_value:
            # 根据你的需求处理code值，这里简单地将其转换为URL格式
            # 实际处理中可能需要更复杂的逻辑来生成正确的URL
            parts = code_value.split('-')
            # 获取最后一个部分
            last_part = parts[-1]
            url = f'https://news.ifai.io/article/{last_part}'
            result.append({'url': url})

    # 将结果转换为JSON格式
    # output_json = json.dumps(result, indent=4, ensure_ascii=False)
    return result

def generateSitemap(data):
    # 创建根元素
    urlset = Element("urlset")
    # 解析JSON数据并创建XML元素
    for entry in data:
        url = SubElement(urlset, "url")
        loc = SubElement(url, "loc")
        loc.text = entry.get("url")

        # 添加其他你需要的元素，比如priority和changefreq
        priority = SubElement(url, "priority")
        priority.text = "0.6"
        changefreq = SubElement(url, "changefreq")
        changefreq.text = "never"
    # 生成格式化的XML字符串
    xml_str = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
    xml_str = xml_str.replace('<?xml version="1.0" ?>\n', '')
    xml_str = xml_str.replace('<urlset>\n', '')
    xml_str = xml_str.replace('\n</urlset>\n', '')
    # 遍历XML树，只处理<url>元素 
    # 生成xml文件
    # print(xml_str)
    generateSiteMapFile(xml_str)

def generateSiteMapFile(xml_str):
    template_file_path = './public/template.xml'
    # 输出修改后的XML到新的文件
    modified_xml_file = json_file_path +'.xml'
    with open(template_file_path, 'r') as file:
        content = file.read()
    new_xml_str = content.replace('<custom_content>Your custom content here</custom_content>', xml_str)
    xml_res = minidom.parseString(new_xml_str).toprettyxml(indent="", newl="")
    with open(modified_xml_file, 'w') as file:
        file.write(xml_res)

def main():
 res_json = generateJSON()
 generateSitemap(res_json)

if __name__ == '__main__':
    main()