import requests
from bs4 import BeautifulSoup
import codecs
import datetime

# 定义一个函数，从本地 txt 文件读取需要爬取的网址
def read_urls_from_file(file_name):
    # 打开文件
    with open(file_name, "r") as f:
        # 读取文件内容，按行分割，去除换行符
        urls = f.read().splitlines()
    # 返回网址列表
    return urls

def automatic_detect(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding  # 先使用 apparent_encoding 猜测编码格式
    soup = BeautifulSoup(res.text, 'html.parser')
    charset = soup.find('meta', {'charset': True})  # 查找 <meta charset="xxx"> 标签
    if charset:  # 如果找到了 <meta> 标签
        charset = charset['charset'].lower()  # 获取 charset 属性的值，并转换为小写
        if codecs.lookup(charset):  # 如果 codecs 模块支持该编码格式
            return charset  # 直接返回该编码格式
    # 如果无法从 <meta> 标签中获取编码格式，或者编码格式不被支持，则使用 apparent_encoding 猜测编码格式
    return res.apparent_encoding

if __name__ == '__main__':
    # 指定本地 txt 文件的路径和名称
    file_name = "urls.txt"
    # 调用函数，从文件中读取网址列表
    urls = read_urls_from_file(file_name)

    # 输出总行数
    print(f"Total urls: {len(urls)}")

    # 循环遍历网址列表，依次爬取每个网址的内容
    for i in range(len(urls)):
        url = urls[i]
        codetype = automatic_detect(url)
        print(f"Processing line {i + 1}: {url}")
        # 伪装头信息的引入
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
        req = requests.get(url=url, headers=header)
        # 返回爬取网站信息

        # 检查请求是否成功
        if req.status_code == 200:
            # 处理请求成功的情况
            print("Success!\n")
        else:
            # 处理请求失败的情况
            # 将失败的 url 写入 fail.txt 文件
            with open("D:/fail.txt", "a") as f:
                f.write(url + "\n")
            # 跳过当前网址，继续下一个网址的爬取
            continue

        req.encoding = codetype
        # 查看head中charset可以查找到编码信息

        html = req.text
        # 转化为文本

        bes = BeautifulSoup(html, "lxml")
        # 把要解析的字符串以标准的缩进格式输出
        pretty = bes.prettify()
        # print(pretty)

        # 使用title作为文件名
        head = bes.find("title").text
        head = head.replace("<title>", "").replace("</title>", "")
        print(head)
        filename = f"D:/{head}.txt"

        # print(bes.get_text())
        webtext = bes.get_text()
        # 获取当前系统时间
        now = datetime.datetime.now()

        # 将网页内容写入文件
        with open(filename, 'w', encoding=req.encoding) as f:
            # 写入文件头部信息
            f.write(f"Url: {url}\n")
            f.write(f"Timestamp: {now}\n\n")
            # 写入网页内容
            f.write(webtext)

    # 输出完成信息
    print("All urls have been processed!")