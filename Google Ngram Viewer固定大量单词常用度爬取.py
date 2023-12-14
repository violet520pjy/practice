import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from retrying import retry

# 从 Excel 文件读取数据
excel_file_path = 'Problem_C_Data_Wordle.xlsx'
df = pd.read_excel(excel_file_path)

# 获取 "Word" 列的值
words_column = df['Word']

# 设置年份范围
year_start = "2009"
year_end = "2019"

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

# 创建文件夹用于保存图表
output_folder = 'ngram_charts'
os.makedirs(output_folder, exist_ok=True)

# 设置重试策略
@retry(wait_fixed=10000, stop_max_attempt_number=3)
def fetch_and_save_chart(word):
    # 构造请求参数
    params = {
        "content": word,
        "year_start": year_start,
        "year_end": year_end
    }

    # 发送请求
    html = requests.get("https://books.google.com/ngrams/json", params=params, headers=headers, timeout=30).text
    time_series = pd.read_json(html, typ="series")
    year_values = list(range(int(year_start), int(year_end) + 1))
    all_y_values = []

    # 创建新图形对象
    plt.figure()

    # 绘制图表
    for series in time_series:
        plt.plot(year_values, series["timeseries"], label=series["ngram"])
        all_y_values.extend(series["timeseries"])

    plt.title(f"Google Books Ngram Viewer - {word}", pad=10)
    plt.xticks(list(range(int(year_start), int(year_end) + 1, 1)))
    plt.grid(axis="y", alpha=0.3)
    plt.ylabel("%", labelpad=5)
    plt.xlabel(f"Year: {year_start}-{year_end}", labelpad=5)

    # 计算并显示平均值
    average_y_values = np.mean(all_y_values)
    plt.text(1.02, 0.5, f'Overall Average: {average_y_values:.7f}%', transform=plt.gca().transAxes, ha='left', va='center', color='black', rotation=90)

    # 保存图表到文件夹
    save_path = os.path.join(output_folder, f"{word}_ngram_chart.png")
    plt.savefig(save_path)
    print(f"图表已保存：{save_path}")

    # 调整图形布局以确保文本显示正常
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # 清空图表以便下一次循环
    plt.clf()

# 遍历每个单词并生成图表
for word in words_column:
    try:
        fetch_and_save_chart(word)
    except Exception as e:
        print(f"处理单词 '{word}' 时发生错误：{e}")
