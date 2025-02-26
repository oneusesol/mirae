import os
import sys
import time
import random
import django
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.db import connections  # 특정 데이터베이스 강제 지정

# Django 환경 설정
sys.path.append("/home/ubuntu/mirae/web/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.models import GoogleNewsCrawling  # Django ORM 모델 import
from api.models import NaverTrend, GoogleTrend, TwitterTrend  # 키워드 테이블 import

# User-Agent 리스트 (자동화 탐지 방지)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

# 기존 크롬 프로세스 종료
os.system("pkill -f chrome || true")

# 기존 데이터 삭제 및 ID 초기화 (Django ORM 사용)
def reset_table():
    with connections["crawling_news_db"].cursor() as cursor:
        cursor.execute("DELETE FROM google_news_crawling;")
        cursor.execute("ALTER TABLE google_news_crawling AUTO_INCREMENT = 1;")
    print("테이블 초기화 완료 (데이터 삭제 + ID 리셋)")

# DB에서 키워드 가져오기 (Django ORM 활용)
def get_keywords():
    keywords = list(NaverTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    keywords += list(GoogleTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    keywords += list(TwitterTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    return list(set(keywords))  # 중복 제거 후 반환

# 데이터 저장 함수 (중복 검사 후 저장)
def save_to_db(title, content, link):
    """Django ORM을 사용하여 뉴스 데이터 저장"""
    if not title or not content or not link:
        print("빈 데이터 발견, 저장하지 않음")
        return  

    # 중복 체크 후 저장
    if not GoogleNewsCrawling.objects.using("crawling_news_db").filter(link=link).exists():
        GoogleNewsCrawling.objects.using("crawling_news_db").create(
            title=title.strip(),
            content=content.strip(),
            link=link.strip()
        )
        print(f"Saved to DB: {title}")
    else:
        print(f"Skipping (Already in DB): {title}")

# Selenium WebDriver 초기화
def initialize_driver():
    """크롬 드라이버 초기화 및 자동화 탐지 방지"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=ko-KR")  # 한국어 설정
    chrome_options.add_argument("--window-size=1920,1080")

    # User-Agent 무작위 변경 (자동화 탐지 우회)
    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f"user-agent={user_agent}")

    # 자동화 탐지 방지
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # `user-data-dir` 문제 해결: 고유한 경로 사용
    unique_profile_dir = f"/tmp/chrome-profile-{os.getpid()}"
    chrome_options.add_argument(f"--user-data-dir={unique_profile_dir}")

    # ChromeDriver 실행
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # DevTools 실행을 통한 자동화 탐지 방지
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

# Google 뉴스 검색 후 모든 뉴스 링크 열고 본문 크롤링
def open_news_links_and_scrape_content(search_query):
    driver = initialize_driver()
    encoded_query = search_query.replace(" ", "%20")
    url = f'https://www.google.com/search?q={encoded_query}&tbm=nws'
    print(f"Searching news for keyword: {search_query} -> {url}")

    driver.get(url)
    time.sleep(random.uniform(3, 7))

    try:
        # 모든 뉴스 링크 찾기
        news_link_elements = driver.find_elements(By.XPATH, "//*[@id='rso']//div/g-section-with-header//a")
        news_links = [element.get_attribute("href") for element in news_link_elements if element.get_attribute("href")]
        print(f"Found {len(news_links)} news articles.")

        for index, news_link in enumerate(news_links):
            try:
                print(f"Opening news link {index + 1}: {news_link}")
                driver.get(news_link)  # 같은 창에서 열기
                time.sleep(random.uniform(3, 7))  # 페이지 로드 대기

                # 뉴스 본문 가져오기
                content_elements = driver.find_elements(By.CSS_SELECTOR, "p")
                news_content = " ".join([element.text for element in content_elements if element.text.strip()])

                # 기사 제목 가져오기
                try:
                    title = driver.find_element(By.TAG_NAME, "h1").text
                except:
                    title = f"News {index + 1}"

                print(f"Extracted News Content for article {index + 1}:")
                print(news_content if news_content else "No content found.")

                # 데이터베이스 저장
                save_to_db(title, news_content, news_link)

                # 검색 결과 창으로 복귀
                driver.back()
                time.sleep(random.uniform(3, 7))

            except Exception as e:
                print(f"Error processing news link {index + 1}: {e}")
                driver.back()
                time.sleep(random.uniform(3, 7))

    except Exception as e:
        print(f"Error locating news links: {e}")

    driver.quit()

# 실행 메인 코드
if __name__ == "__main__":
    reset_table()
    keywords = get_keywords()
    for keyword in keywords:
        print(f"Searching news for keyword: {keyword}")
        open_news_links_and_scrape_content(keyword)
