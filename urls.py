import requests
from bs4 import BeautifulSoup
import time

url = "https://   "
depth = 0
max_depth = 10
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com'}

def crawl(url, depth):
    if depth > max_depth:
        return

    count = 0  # 初始化计数器变量
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith("https://   ") and href != url:
                with open('pythonjishuurls.txt', 'a') as f:
                    f.write(href + '\n')
                count += 1  # 每找到一个新的链接，计数器加一
                print(f"{count} {href} founded!")
                crawl(href, depth + 1)
    except Exception as e:
        print("Error:", e)

    time.sleep(1)  # 增加请求间隔时间，避免被目标网站检测为爬虫并限制访问

crawl(url, depth)