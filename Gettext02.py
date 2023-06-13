import requests
from bs4 import BeautifulSoup
import re
import codecs
import datetime
import time
import pickle

# 定义一个函数，从本地 txt 文件读取需要爬取的网址
def read_urls_from_file(file_name):
# 打开文件
    with open(file_name, "r") as f:
# 读取文件内容，按行分割，去除换行符
        urls = f.read().splitlines()
# 返回网址列表
    return urls

    #自动获取网站编码
    #def automatic_detect(url):
    #    res = requests.get(url)
    #    return res.apparent_encoding

#设置超时时间
timeout = 3

def automatic_detect(url):
    res = requests.get(url, timeout=timeout)
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
    file_name = "sitemap_urls.txt"
    # 调用函数，从文件中读取网址列表
    urls = read_urls_from_file(file_name)
    # 遍历网址列表

    # 输出总行数
    print(f"Total urls: {len(urls)}")

    #爬取
    for i in range(len(urls)):
        url = urls[i]
        print(f"Processing line {i + 1}: {url}")
        try:
            
            codetype = automatic_detect(url)

            print("Codetype: %s" % codetype)  
            #伪装头信息的引入
            #header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"}
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'    }
            req = requests.get(url=url,headers = header, timeout=timeout) 
            #req = requests.get(url=url)
            #返回爬取网站信息

            # 检查请求是否成功
            if req.status_code == 200:
                # 处理请求成功的情况
                print("Success!\n")
            else:
                # 处理请求失败的情况
                # 将失败的 url 写入 fail.txt 文件
                with open("D:/fail.txt", "a") as f:
                    f.write(url + "\n")

            req.encoding = codetype  
            #查看head中charset可以查找到编码信息

            html = req.text 
            #转化为文本

            bes = BeautifulSoup(html,"lxml")
            #把要解析的字符串以标准的缩进格式输出
            pretty = bes.prettify()
            #print(pretty)

            import re

            # 获取标题并清洗
            head = bes.find("title").text
            head = head.replace("<title>", "").replace("</title>", "")

            # 替换文件名中的非法字符
            illegal_chars = r'[<>:"/\\|?*]'
            head = re.sub(illegal_chars, '_', head)

            # 截断文件名以避免过长
            max_filename_length = 260  # Windows系统的文件名长度限制为260个字符
            if len(head) > max_filename_length:
                head = head[:max_filename_length - 4] + '...'

            # 构建文件名并输出
            filename = f"D:\\{head}.txt"
            print(filename)

            #print(bes.get_text())
            webtext = bes.get_text()
            # 获取当前系统时间
            now = datetime.datetime.now()
            dxh = "由杜肖瀚制作"
            # 构造 head 字符串
            head = f"url: {url}\n"
            head += f"time: {now}\n"
            head += f"dxh: {dxh}\n\n"

            with codecs.open(filename,"w",encoding=codetype) as file:    ##打开读写文件，逐行将列表读入文件内
                file.write(head)
                for line in webtext:
                    # 将特殊字符替换为其他字符
                    line = line.replace('\xa0', ' ')
                    file.write(line)

            #覆写去除多余的换行符
            with codecs.open(filename, "r", encoding=codetype) as f:
                lines = f.readlines()
            new_lines = []
            for i in range(len(lines)):
                if i == 0:
                    new_lines.append(lines[i])
                elif lines[i] != '\n' or lines[i-1] != '\n':
                    new_lines.append(lines[i])
            with codecs.open(filename, "w", encoding=codetype) as f:
                f.writelines(new_lines)

            time.sleep(1)  # 增加请求间隔时间，避免被目标网站检测为爬虫并限制访问
        except requests.exceptions.Timeout:
            # 如果请求超时，跳过当前循环
            print(f"请求 {url} 超时，跳过当前循环")
            with open("D:/fail.txt", "a") as f:
                    f.write("请求超时，跳过当前循环"+url + "\n")
            continue

        except requests.exceptions.RequestException as e:
            # 处理其他异常
            print(f"请求 {url} 出错：{e}")
            with open("D:/fail.txt", "a") as f:
                    f.write("请求出错，跳过当前循环"+url + "\n")
            continue
