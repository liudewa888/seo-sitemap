import json
from xml.etree.ElementTree import Element, SubElement, tostring, parse,fromstring,ElementTree
from xml.dom import minidom
import requests
namespaces = {
    'html': 'http://www.w3.org/1999/xhtml',
    'xhtml': 'http://www.w3.org/1999/xhtml'
}


json_dir_path = './public/'
headers={
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}
def generateJSON():
    # global headers
    # url = 'https://api.ifai.io/protal/codes'
    # res = requests.get(url,headers=headers).json()
    # if 'data' not in res:
    #   return
    result = []
    result1 =[]
    result2 = []
    json_file_path = json_dir_path + 'template.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
     res = json.load(file)
    for item in res.get('data', []):
        code_value = item.get('code')
        date = item.get('insertTime')
        changefreq = item.get('changefreq')
        priority = item.get('priority')
        if date:
            obj = {
               'code': code_value,
               'date': date,
               'changefreq': changefreq,
               'priority': priority
               }
            result1.append(obj)

    json_file_path = json_dir_path + 'codes.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
    # 读取整个文件，并将内容转换为Python的字典对象
     res = json.load(file)
    # 解析原始数据，并构造所需的格式
    for item in res.get('data', []):
        code_value = item.get('code')
        date = item.get('insertTime')
        if code_value:
            obj = {
               'code': code_value,
               'date': date,
               'changefreq': 'weekly',
               'priority': '0.6'
               }
            result2.append(obj)

    result.append(result1)
    result.append(result2)
    # 将结果转换为JSON格式
    # output_json = json.dumps(result, indent=4, ensure_ascii=False)
    return result

def generateSitemap(data):
    # template_file_path = json_dir_path +'template.xml'
    # with open(template_file_path, 'r') as file:
    #     content = file.read()
    # tree = fromstring(content)
    # for elem in tree.iter():
    #     if elem.tag.endswith('urlset'):
    #         urlset = elem
    # urlset = root.find('url')
    # print(urlset,900)

    # 创建根元素
    urlset = Element("urlset",{
    'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    'xmlns:xhtml': 'http://www.w3.org/1999/xhtml'
    })



    # 解析JSON数据并创建XML元素
    for entry in data[0]:
        code = entry.get("code")
        link_en = "https://news.ifai.io" 
        link_zh = "https://news.ifai.io/zh"
        link_ja = "https://news.ifai.io/ja"

        url = SubElement(urlset, "url")
        loc = SubElement(url, "loc")
        loc.text = link_en + code
        # 添加其他你需要的元素，比如priority和changefreq
        lastmod = SubElement(url, "lastmod")
        lastmod.text = entry.get("date")
        changefreq = SubElement(url, "changefreq")
        changefreq.text = entry.get("changefreq")
        priority = SubElement(url, "priority")
        priority.text = entry.get("priority")
        xhtml1 = SubElement(url, "{http://www.w3.org/1999/xhtml}link")
        xhtml1.set("href",  link_ja)
        xhtml1.set("hreflang", "ja")
        xhtml1.set("rel", "alternate")
        xhtml2 = SubElement(url, "{http://www.w3.org/1999/xhtml}link")
        xhtml2.set("href", link_zh)
        xhtml2.set("hreflang", "zh")
        xhtml2.set("rel", "alternate")
        xhtml3 = SubElement(url, "{http://www.w3.org/1999/xhtml}link")
        xhtml3.set("href", link_en)
        xhtml3.set("hreflang", "en")
        xhtml3.set("rel", "alternate")
    # 解析JSON数据并创建XML元素
    for entry in data[1]:
        code = entry.get("code")
        link_en = "https://news.ifai.io/" + code
        link_zh = "https://news.ifai.io/zh/" + code
        link_ja = "https://news.ifai.io/ja/" + code

        url = SubElement(urlset, "url")
        loc = SubElement(url, "loc")
        loc.text = link_en
        # 添加其他你需要的元素，比如priority和changefreq
        lastmod = SubElement(url, "lastmod")
        lastmod.text = entry.get("date")
        changefreq = SubElement(url, "changefreq")
        changefreq.text = "weekly"
        priority = SubElement(url, "priority")
        priority.text = "0.6"
        xhtml1 = SubElement(url, "{http://www.w3.org/1999/xhtml}link")
        xhtml1.set("href",  link_ja)
        xhtml1.set("hreflang", "ja")
        xhtml1.set("rel", "alternate")
        xhtml2 = SubElement(url, "{http://www.w3.org/1999/xhtml}link")
        xhtml2.set("href",  link_zh)
        xhtml2.set("hreflang", "zh")
        xhtml2.set("rel", "alternate")
        xhtml3 = SubElement(url, "{http://www.w3.org/1999/xhtml}link")
        xhtml3.set("href", link_en)
        xhtml3.set("hreflang", "en")
        xhtml3.set("rel", "alternate")

    # 生成格式化的XML字符串
    xml_str = tostring(urlset, encoding="unicode", method="xml")
    # xml_str = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
    # xml_str = xml_str.replace('<?xml version="1.0" ?>\n', '')
    # xml_str = xml_str.replace('<urlset>\n', '')
    # xml_str = xml_str.replace('\n</urlset>\n', '')
    # 遍历XML树，只处理<url>元素 
    # 生成xml文件
    # print(xml_str)
    generateSiteMapFile(xml_str)

def generateSiteMapFile(xml_str):
    # template_file_path = json_dir_path +'template.xml'
    # 输出修改后的XML到新的文件
    modified_xml_file =  json_dir_path + 'ainews_sitemap.xml'
    # with open(template_file_path, 'r') as file:
    #     content = file.read()
    # new_xml_str = content.replace('<custom_content>Your custom content here</custom_content>', xml_str)
    new_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ", newl="\n")
    with open(modified_xml_file, 'w') as file:
        file.write(new_xml_str)

def main():
 res_json = generateJSON()
 generateSitemap(res_json)

if __name__ == '__main__':
    main()