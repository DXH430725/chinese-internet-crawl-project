import requests
from bs4 import BeautifulSoup

url = 'https://pythonjishu.com/sitemap_index.xml'
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com'}

def get_sitemap_urls(url):
    try:
        response = requests.get(url, headers=headers)
        print(response)  # 调试信息：输出响应状态码
        soup = BeautifulSoup(response.text, 'xml')
        urls = []
        for sitemap in soup.find_all('sitemap'):
            sitemap_url = sitemap.find('loc').text
            urls += get_sitemap_urls(sitemap_url)
        for url in soup.find_all('url'):
            loc = url.find('loc').text
            urls.append(loc)
        return urls
    except Exception as e:
        print("Error:", e)

urls = get_sitemap_urls(url)
print(urls)  # 调试信息：输出所有解析出来的 URL
with open('sitemap_urls.txt', 'w') as f:
    for url in urls:
        f.write(url + '\n')
print("Done!")  # 调试信息：输出程序执行完毕的信息