import hashlib
import datetime
import requests

def encrypt_with_md5(string_to_encrypt):
    # 获取今天的日期（不包含年份和月份）
    today_date = datetime.datetime.now().strftime("%d")
    
    # 将字符串连接起来
    combined_string = string_to_encrypt + today_date
    
    # 创建MD5对象
    md5_obj = hashlib.md5()
    
    # 对字符串进行编码，然后更新MD5对象
    md5_obj.update(combined_string.encode('utf-8'))
    
    # 返回MD5加密后的十六进制字符串
    return md5_obj.hexdigest()


def request():
    url = 'https://news.ifai.io/api/sitemap'
    cookie_dict = {
    'token': encrypt_with_md5('ifai'),
    }
    res = requests.get(url, cookies=cookie_dict).json()
    print(res)

def main():
    request()

if __name__ == '__main__':
    main()