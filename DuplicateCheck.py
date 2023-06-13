import hashlib
import time

def get_md5(url):
    """计算 URL 的 MD5 值"""
    return hashlib.md5(url.encode()).hexdigest()

def check_duplicate(file):
    """检查文件中的 URL 是否重复"""
    url_set = set()  # 存储 URL 的哈希值
    duplicate_count = 0  # 重复 URL 的数量

    with open(file, 'r') as f:
        lines = f.readlines()
        n = len(lines)
        print(f"查重开始，共有{n}条URL。")
        for line in lines:
            url = line.strip()
            url_hash = get_md5(url)
            if url_hash in url_set:
                duplicate_count += 1
            else:
                url_set.add(url_hash)

    return duplicate_count

if __name__ == '__main__':
    start_time = time.time()
    duplicate_count = check_duplicate('pythonjishuurls.txt')
    end_time = time.time()
    elapsed_time = end_time - start_time
    n = sum(1 for line in open('pythonjishuurls.txt'))
    duplicate_rate = duplicate_count / n
    print(f"查重结束，用时{elapsed_time:.3f}s，共有{duplicate_count}条重复URL，重复率为{duplicate_rate:.3%}。")