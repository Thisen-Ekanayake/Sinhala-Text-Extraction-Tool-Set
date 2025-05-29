from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chromedriver_path = r"C:\Users\user\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

url = "https://www.lankadeepa.lk/latest_news/%E0%B6%86%E0%B6%B1%E0%B6%BA%E0%B6%B1%E0%B6%BA-%E0%B6%9A%E0%B7%85-%E0%B6%BD%E0%B6%AB-%E0%B6%B8%E0%B6%A7%E0%B6%BB%E0%B6%9A%E0%B6%A7%E0%B6%B1-2800-%E0%B6%9A-%E0%B7%80%E0%B7%85%E0%B6%B3%E0%B6%B4%E0%B7%85%E0%B6%A7/1-672951"
driver.get(url)
time.sleep(3)  # Wait for page to load

try:
    # Inspect and adjust selector as needed:
    article = driver.find_element(By.CSS_SELECTOR, "div.article-content")
    print(article.text)
except Exception as e:
    print("Could not find article content:", e)

driver.quit()
