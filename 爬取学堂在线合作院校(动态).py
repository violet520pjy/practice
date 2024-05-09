from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json

def scrape_xuetangx(url):
    # 初始化 WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # 点击导航到合作院校的链接
    try:
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/university/all"]'))
        )
        link.click()
        # 切换到新打开的标签页
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
    except TimeoutException:
        print("Timeout waiting for the university page link.")
        driver.quit()
        return []

    # 在新页面上提取数据
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.school'))
        )
        schools = driver.find_elements(By.CSS_SELECTOR, 'div.school')
        data = []
        for school in schools:
            school_name_cn = school.find_element(By.CSS_SELECTOR, 'p.name_cn').text.strip()
            school_name_en = school.find_element(By.CSS_SELECTOR, 'p.name_en').text.strip()
            course_count = school.find_element(By.CSS_SELECTOR, 'p.count').text.strip()
            data.append({
                'school_name_cn': school_name_cn,
                'school_name_en': school_name_en,
                'courses_count': course_count
            })
    finally:
        driver.quit()

    return data

def main():
    url = 'https://v1-www.xuetangx.com'
    schools_data = scrape_xuetangx(url)
    print("Extracted data: ", schools_data)

    # 保存数据到 JSON 文件
    if schools_data:
        with open('xuetangx_partners.json', 'w', encoding='utf-8') as file:
            json.dump(schools_data, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
