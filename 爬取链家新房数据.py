import requests
from bs4 import BeautifulSoup
import json


def scrape_lianjia(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到包含楼盘数据的HTML元素
    data = []
    for item in soup.find_all('div', class_='resblock-desc-wrapper'):
        name = item.find('a', class_='name').text.strip()  # 楼盘名称
        price = item.find('span', class_='number').text.strip()  # 价格
        size = item.find('div', class_='resblock-area').find('span').text.strip()  # 平米数

        data.append({
            'name': name,
            'price': price,
            'size': size
        })

    return data


def main():
    base_url = 'https://bj.fang.lianjia.com/loupan/pg'
    all_data = []
    # 只爬取前3页的数据
    for page in range(1, 4):
        url = f'{base_url}{page}'
        all_data.extend(scrape_lianjia(url))

    # 将数据保存到JSON文件
    with open('lianjia_data.json', 'w', encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
