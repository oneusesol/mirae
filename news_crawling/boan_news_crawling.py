import os
import sys
import time
import random
import django
from datetime import datetime
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

from api.models import BoanNewsCrawling  # Django ORM 모델 import
from api.models import NaverTrend, GoogleTrend, TwitterTrend  # 키워드 테이블 import

# User-Agent 리스트 (자동화 탐지 우회)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

# 기존 크롬 프로세스 종료
os.system("pkill -f chrome || true")
time.sleep(3)  # 프로세스 종료 대기

# 기존 데이터 삭제 및 ID 초기화
def reset_table():
    with connections["crawling_news_db"].cursor() as cursor:
        cursor.execute("DELETE FROM boan_news_crawling;")
        cursor.execute("ALTER TABLE boan_news_crawling AUTO_INCREMENT = 1;")
    print("테이블 초기화 완료 (데이터 삭제 + ID 리셋)")

# DB에서 키워드 가져오기
def get_keywords():
    keywords = list(NaverTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    keywords += list(GoogleTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    keywords += list(TwitterTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    return list(set(keywords))  # 중복 제거 후 반환

# 데이터 저장 함수
def save_to_db(title, content, link):
    """Django ORM을 사용하여 뉴스 데이터 저장"""
    if not title or not content or not link:
        print("빈 데이터 발견, 저장하지 않음")
        return  

    # 중복 체크 후 저장
    if not BoanNewsCrawling.objects.using("crawling_news_db").filter(link=link).exists():
        BoanNewsCrawling.objects.using("crawling_news_db").create(
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
    
    # 기존 Chrome 프로세스 강제 종료 (완전 종료 확인)
    os.system("pkill -f chrome || true")
    time.sleep(3)  # 잠시 대기하여 프로세스 종료 확인

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

    # ChromeDriver 실행
    service = Service("/usr/local/bin/chromedriver")
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # DevTools 실행을 통한 자동화 탐지 방지
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    except Exception as e:
        print(f"ChromeDriver 실행 오류: {e}")
        sys.exit(1)  # 프로그램 강제 종료
    
    return driver

# 보안뉴스 검색 후 뉴스 본문 크롤링
def search_boannews_and_scrape_results(search_query):
    driver = initialize_driver()
    search_url = "https://www.boannews.com/search/list.asp"

    driver.get(search_url)
    time.sleep(random.uniform(3, 7))  # 랜덤 대기 시간 추가

    try:
        search_input = driver.find_element(By.NAME, "find")
        search_input.clear()
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.RETURN)
        time.sleep(random.uniform(3, 7))

        # 검색 결과 크롤링
        news_elements = driver.find_elements(By.CSS_SELECTOR, "div.news_list")
        today_date = datetime.today().strftime("%Y년 %m월 %d일")
        news_links = set()
        
        for news in news_elements:
            try:
                link_element = news.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")
                date_element = news.find_element(By.CLASS_NAME, "news_writer")
                date_text = " ".join(date_element.text.split("|")[-1].strip().split(" ")[:3])

                if today_date == date_text:
                    news_links.add(link)
            except:
                print("기사 링크 없음 또는 날짜 정보 없음")

        if not news_links:
            print(f"'{search_query}' 검색어에 대한 수집된 뉴스가 없습니다.")
            return

        for index, news_link in enumerate(news_links):
            try:
                print(f"\n[{index+1}] Opening News Link: {news_link}")

                driver.execute_script(f"window.open('{news_link}', '_blank');")
                time.sleep(random.uniform(3, 7))

                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(random.uniform(3, 7))

                try:
                    title = driver.find_element(By.TAG_NAME, "h1").text
                    article_body = driver.find_element(By.XPATH, "//*[@id='news_content']").text

                    print("Article Title:", title)
                    print("Article Content:", article_body[:500])

                    save_to_db(title, article_body, news_link)

                except:
                    print("Failed to retrieve article content.")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(random.uniform(3, 7))

            except:
                print(f"Error processing news link {index+1}")

        print("Crawling completed.")

    except Exception as e:
        print(f"Error during search: {e}")

    driver.quit()

# 실행 메인 코드
if __name__ == "__main__":
    reset_table()
    keywords = get_keywords()
    for keyword in keywords:
        print(f"Searching news for keyword: {keyword}")
        search_boannews_and_scrape_results(keyword)
