import os
import sys
import time
import random
import django
from itertools import chain
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from django.db import connections

# Django 환경 설정
sys.path.append("/home/ubuntu/mirae/web/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.models import GoogleNewsCrawling, NaverTrend, GoogleTrend, TwitterTrend

# User-Agent 리스트 (자동화 탐지 방지)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

# 기존 데이터 삭제 및 ID 초기화
def reset_table():
    with connections["crawling_news_db"].cursor() as cursor:
        cursor.execute("DELETE FROM google_news_crawling;")
        cursor.execute("ALTER TABLE google_news_crawling AUTO_INCREMENT = 1;")
    print("테이블 초기화 완료 (데이터 삭제 + ID 리셋)")

# DB에서 키워드 가져오기 (최적화)
def get_keywords():
    all_keywords = list(chain(
        NaverTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True),
        GoogleTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True),
        TwitterTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True),
    ))
    return list(set(map(str.lower, all_keywords)))  # 대소문자 무시 중복 제거

# 데이터 저장 (중복 검사 후 저장)
def save_to_db(title, content, link):
    if not title or not content or not link:
        print("빈 데이터 발견, 저장하지 않음")
        return

    if not GoogleNewsCrawling.objects.using("crawling_news_db").filter(link=link).exists():
        GoogleNewsCrawling.objects.using("crawling_news_db").create(
            title=title.strip(),
            content=content.strip(),
            link=link.strip()
        )
        print(f"Saved to DB: {title}")
    else:
        print(f"Skipping (Already in DB): {title}")

# Selenium WebDriver 초기화 (최적화)
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=ko-KR")
    chrome_options.add_argument("--window-size=1920,1080")

    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    unique_profile_dir = f"/tmp/chrome-profile-{os.getpid()}"
    chrome_options.add_argument(f"--user-data-dir={unique_profile_dir}")

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

# Google 뉴스 검색 후 모든 뉴스 링크 열고 본문 크롤링 (최적화)
def open_news_links_and_scrape_content(driver, search_query):
    encoded_query = search_query.replace(" ", "%20")
    url = f'https://www.google.com/search?q={encoded_query}&tbm=nws&tbs=qdr:d'
    print(f"Searching news for keyword: {search_query} -> {url}")

    driver.get(url)
    time.sleep(random.uniform(3, 7))  # 대기 시간 최적화

    try:
        news_links = []
        for count in range(1, 11):
            xpath = f"//*[@id='rso']/div/div/div[{count}]/div/div/a"
            link_elements = driver.find_elements(By.XPATH, xpath)
            if not link_elements:
                break

            for element in link_elements:
                href = element.get_attribute("href")
                if href and href not in news_links:
                    news_links.append(href)

        print(f"Found {len(news_links)} news articles.")

        for index, news_link in enumerate(news_links):
            try:
                print(f"Opening news link {index + 1}: {news_link}")
                driver.execute_script(f"window.open('{news_link}', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(random.uniform(1, 3))

                content_elements = driver.find_elements(By.CSS_SELECTOR, "p")
                news_content = " ".join([element.text for element in content_elements if element.text.strip()])

                title_elements = driver.find_elements(By.TAG_NAME, "h1")
                title = title_elements[0].text if title_elements else f"News {index + 1}"

                save_to_db(title, news_content, news_link)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])  # 검색 결과 페이지로 복귀
            except Exception as e:
                print(f"Error processing news link {index + 1}: {e}")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        print(f"Error locating news links: {e}")

# 실행 메인 코드 (드라이버 재사용 적용)
if __name__ == "__main__":
    reset_table()
    keywords = get_keywords()
    
    driver = initialize_driver()  # 드라이버 한 번만 실행
    try:
        for keyword in keywords:
            print(f"Searching news for keyword: {keyword}")
            open_news_links_and_scrape_content(driver, keyword)
    finally:
        driver.quit()  # 실행 완료 후 종료
