# 샘플 코드 수정 필요

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Selenium WebDriver 초기화
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # GPU 사용 방지 (메모리 절약)
    chrome_options.add_argument("--window-size=1920,1080")  # 브라우저 크기 지정
    # chrome_options.add_argument("--headless")  # 필요하면 활성화

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

# Google 뉴스 검색 후 모든 뉴스 링크 하나씩 열고 본문 크롤링
def open_news_links_one_by_one_and_scrape_content(search_query):
    driver = initialize_driver()
    encoded_query = search_query.replace(" ", "%20")
    url = f'https://www.google.com/search?q={encoded_query}&tbm=nws'
    print(f"Searching news for keyword: {search_query} -> {url}")

    driver.get(url)
    time.sleep(3)

    try:
        # 검색 결과 창 저장
        original_window = driver.current_window_handle

        # 모든 뉴스 링크 찾기 (XPath 사용)
        news_link_elements = driver.find_elements(By.XPATH, "//*[@id='rso']//div/g-section-with-header//a")
        news_links = [element.get_attribute("href") for element in news_link_elements if element.get_attribute("href")]
        print(f"Found {len(news_links)} news articles.")
        
        for index, news_link in enumerate(news_links):
            try:
                print(f"Opening news link {index + 1}: {news_link}")
                driver.get(news_link)  # 같은 창에서 열기
                time.sleep(3)  # 페이지 로드 대기
                
                # 뉴스 본문 가져오기
                content_elements = driver.find_elements(By.CSS_SELECTOR, "p.text[style='font-size:18px']")
                news_content = " ".join([element.text for element in content_elements if element.text.strip()])
                
                print(f"Extracted News Content for article {index + 1}:")
                print(news_content if news_content else "No content found.")
                
                # 검색 결과 창으로 복귀
                driver.back()
                time.sleep(3)
            except Exception as e:
                print(f"Error processing news link {index + 1}: {e}")
                driver.back()
                time.sleep(3)
    except Exception as e:
        print(f"Error locating news links: {e}")
    
    time.sleep(5)
    driver.quit()

# 실행 메인 코드
if __name__ == "__main__":
    keyword = "이승환 구미시장 헌법소원"  # 원하는 검색어 입력
    open_news_links_one_by_one_and_scrape_content(keyword)
